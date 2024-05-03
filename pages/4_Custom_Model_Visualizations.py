import numpy as np
import pandas as pd
import streamlit as st

from database import init_db
from database.models import Document
from sqlalchemy import func

from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP

st.set_page_config(
    page_title="Custom Model Visualizations",
    page_icon="📊",
    layout="wide",
)


def visualize_topic_model(topic_model, docs, embeddings):
    # Run the visualization with the original embeddings
    reduced_embeddings = UMAP(
        n_neighbors=10, n_components=2, min_dist=0.0, metric="cosine"
    ).fit_transform(embeddings)

    visualizations = [
        (
            "Hierarchical Documents and Topics",
            topic_model.visualize_documents(
                docs,
                reduced_embeddings=reduced_embeddings,
            ),
        ),
        ("Topic Word Score", topic_model.visualize_barchart()),
        ("Similarity Matrix", topic_model.visualize_heatmap()),
    ]

    for title, viz in visualizations:
        viz.update_layout(
            title_font=dict(color="white"),
            hoverlabel=dict(bgcolor="black"),
            width=800,
            height=800,
            title=title,
        )
        st.plotly_chart(viz)

    # Visualize Topic Probability Distribution
    topic_distr, _ = topic_model.approximate_distribution(docs, min_similarity=0)
    visualize_distribution(topic_model, topic_distr, docs)

    # Visualize Approximate Distribution
    topic_distr, topic_token_distr = topic_model.approximate_distribution(
        docs, calculate_tokens=True
    )
    visualize_approximate_distribution(topic_model, docs[1], topic_token_distr[1])


def visualize_distribution(topic_model, topic_distr, docs):
    topic_options = [f"Topic {i}" for i in range(len(topic_distr))]
    selected_topic = st.selectbox("Select a topic:", topic_options)

    if selected_topic:
        topic_index = int(selected_topic.split(" ")[1])
        viz = topic_model.visualize_distribution(topic_distr[topic_index])
        viz.update_layout(
            title_font=dict(color="white"),
            hoverlabel=dict(bgcolor="black"),
            width=800,
            height=800,
            title=f"Topic {topic_index} Probability Distribution",
        )
        st.plotly_chart(viz)


def visualize_approximate_distribution(topic_model, doc, topic_token_distr):
    df = topic_model.visualize_approximate_distribution(doc, topic_token_distr)
    st.write(df)


st.title("Custom Model Visualizations")

doc_db = init_db()
doc_session = doc_db.Session()

# Model selection dropdown
model_list = (
    doc_session.query(Document.model_names, Document.batch_number)
    .group_by(Document.model_names)
    .all()
)
if not model_list:
    st.warning("No documents available for visualization.")
    if st.button("Upload documents", type="primary"):
        st.switch_page("pages/2_Upload_Documents.py")
    st.stop()
model_list = set([model[0] for model in model_list])
model_list.discard("Not available for documents upload")
model_list = list(model_list)

selected_model = st.selectbox("Pick a model:", model_list)

# find batch that matches model
selected_batch = None
for model in model_list:
    if model == selected_model:
        selected_batch = (
            doc_session.query(Document.batch_number)
            .filter(Document.model_names == model)
            .first()
        )
        if selected_batch:
            selected_batch = selected_batch[0]
        break
else:
    st.warning("No documents available for visualization.")
    st.stop()

if st.button(
    "Visualize training documents",
    key="visualize_docs_btn",
    disabled=selected_model is None,
):
    document_list = (
        doc_session.query(Document)
        .filter(Document.batch_number == selected_batch)
        .all()
    )
    docs = [doc.content for doc in document_list]
    print(docs[:2])  # view format of docs

    with st.spinner("Creating your visualizations:"):

        model = BERTopic.load(selected_model)

        # an example docs:
        # docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data'][:1000]

        sentence_model = model.embedding_model
        # sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        pbar = st.progress(0, "Embedding documents...")
        embeddings = []
        batch_size = 32
        for i in range(0, len(docs), batch_size):
            embeddings.extend(sentence_model.embed(docs[i : i + batch_size]))
            pbar.progress(0.9 * i / len(docs), "Embedding documents...")
        embeddings = np.array(embeddings)
        pbar.progress(0.9, "Creating visualizations...")

        # Visualize
        visualize_topic_model(model, docs, embeddings)
        pbar.progress(1.0)
