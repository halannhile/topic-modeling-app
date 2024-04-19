import streamlit as st
from nlp.topic_modeling import get_pretrained_model, transform_doc_pretrained
from nlp.topic_visualizations import visualize_topics

from database import init_db
from database.models import Document
from sqlalchemy import func

from umap import UMAP

st.set_page_config(
    page_title="Topic Modeling Visualizations",
    page_icon="📊",
    layout="wide",
)


def display_single_visualizations(model_path, texts):

    model = get_pretrained_model(model_path)

    plot_title = f"Topic Bubbles for Pretrained Model"

    topic_vis = visualize_topics(
        model,
        topics=None,
        top_n_topics=40,
        custom_labels=False,
        title=plot_title,
        width=800,
        height=800,
        new_documents=texts,
    )
    topic_vis.update_layout(
        title_font=dict(color="white"),
        hoverlabel=dict(bgcolor="black"),
        width=800,
        height=800,
    )

    st.plotly_chart(topic_vis)


def display_dataset_visualizations(model_path, texts):

    model = get_pretrained_model(model_path)

    embeddings = model.embedding_model.embed(texts)
    reduced_embeddings = UMAP(
        n_neighbors=10, n_components=2, min_dist=0.0, metric="cosine"
    ).fit_transform(embeddings)
    doc_vis = model.visualize_documents(texts, reduced_embeddings=reduced_embeddings)
    doc_vis.update_layout(title_font=dict(color="white"), width=800, height=800)
    st.plotly_chart(doc_vis)


if __name__ == "__main__":

    st.title("Topic Modeling Visualizations")

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
    model_list = set([model[0] for model in model_list])
    model_list.discard("Not available for documents upload")
    model_list = ["BERTopic Wikipedia"] + list(model_list)

    selected_model = st.selectbox("Pick a model:", model_list)
    if selected_model == "BERTopic Wikipedia":
        selected_model = "MaartenGr/BERTopic_Wikipedia"

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
        texts = [doc.content for doc in document_list]

        if len(texts) == 1:
            idx, probs, topic = transform_doc_pretrained(
                document_list[0], selected_model
            )
            txt = st.text_area(
                f"You selected a single document: {document_list[0].filename}\n\n The model classifies it as the topic {topic} with {round(probs*100, 3)}% probability:",
                texts[0],
                height=None if len(texts[0]) < 2000 else 500,
            )
            with st.spinner("Creating your visualizations:"):
                display_single_visualizations(selected_model, texts)
        else:
            st.markdown(
                "You selected a dataset. Visualizing document representations may take a while:"
            )
            with st.spinner("Creating dataset visualizations:"):
                display_dataset_visualizations(selected_model, texts)
