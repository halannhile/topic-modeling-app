import pandas as pd
import streamlit as st

from database import init_db
from database.models import Document
from sqlalchemy import func

from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP


def visualize_topic_model(topic_model, docs, embeddings):
    # Run the visualization with the original embeddings
    reduced_embeddings = UMAP(
        n_neighbors=10, n_components=2, min_dist=0.0, metric="cosine"
    ).fit_transform(embeddings)

    visualizations = [
        (
            "Hierarchical Documents and Topics",
            topic_model.visualize_documents(
                docs, reduced_embeddings=reduced_embeddings
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


if __name__ == "__main__":
    st.title("Even More Bertopic Visualizations")

    doc_db = init_db()
    doc_session = doc_db.Session()

    # Document selection dropdown
    batchnum_list = (
        doc_session.query(Document.batch_number, func.count(Document.batch_number))
        .group_by(Document.batch_number)
        .all()
    )
    if not batchnum_list:
        st.warning("No documents available for visualization.")
        if st.button("Upload documents", type="primary"):
            st.switch_page("pages/2_Upload_Documents.py")
        st.stop()
    batchnum_list = [f"Group {b[0]} ({b[1]} documents)" for b in batchnum_list]
    selected_batch_option = st.selectbox("Pick documents to visualize:", batchnum_list)
    if not selected_batch_option:
        selected_batch_option = batchnum_list[0]

    # Model selection dropdown
    model_list = (
        doc_session.query(Document.model_names).group_by(Document.model_names).all()
    )
    model_list = set(["BERTopic Wikipedia"])
    model_list = list(model_list)

    selected_model = st.selectbox("Pick a model:", model_list)

    if st.button(
        "Visualize documents!",
        key="visualize_docs_btn",
        disabled=selected_model is None,
    ):
        document_list = (
            doc_session.query(Document)
            .filter(Document.batch_number == selected_batch_option.split(" ")[1])
            .all()
        )
        docs = [doc.content for doc in document_list]
        print(docs[:2])  # view format of docs

        with st.spinner("Creating your visualizations:"):

            # an example docs:
            # docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data'][:1000]

            sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = sentence_model.encode(docs, show_progress_bar=False)

            # Train BERTopic
            topic_model = BERTopic().fit(docs, embeddings)

            # Visualize
            visualize_topic_model(topic_model, docs, embeddings)
