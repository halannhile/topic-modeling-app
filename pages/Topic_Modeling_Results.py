import pandas as pd
import streamlit as st
from nlp.topic_modeling import get_pretrained_model, transform_doc_pretrained
from nlp.topic_visualizations import visualize_topics

from database import init_db
from database.models import Document
from sqlalchemy import func

from bertopic import BERTopic

def display_visualizations(model, texts):

    if not model:
        model = get_pretrained_model()

    plot_title = f"Topic Bubbles for BERTopicWikipedia"

    topic_vis = visualize_topics(model,
                                    topics=None,
                                    top_n_topics=40,
                                    custom_labels=False,
                                    title=plot_title,
                                    width=800,
                                    height=800,
                                    new_document=texts[0])
    topic_vis.update_layout(
                                    title_font=dict(color="white"),
                                    hoverlabel=dict(bgcolor="black"),
                                    width = 800,
                                    height = 800)
                                    
    st.plotly_chart(topic_vis)
    
    # doc_vis = model.visualize_documents(texts)
    # st.plotly_chart(doc_vis)

if __name__ == "__main__":

    st.title("Topic Modeling Visualizations")

    doc_db = init_db("sqlite:///db3.db")
    doc_session = doc_db.Session()

    # Document selection dropdown
    batchnum_list = doc_session.query(Document.batch_number, func.count(Document.batch_number)) \
                            .group_by(Document.batch_number).all()
    batchnum_list = [f"Group {b[0]} ({b[1]} documents)" for b in batchnum_list]
    selected_batch_option = st.selectbox("Pick documents to visualize:", batchnum_list)

    # Model selection dropdown
    model_list = doc_session.query(Document.model_names).group_by(Document.model_names).all()
    model_list = ["BERTopic Wikipedia"] + [model[0] for model in model_list]
    selected_model = st.selectbox("Pick a model:", model_list)

    if st.button("Visualize documents!", key="visualize_docs_btn"):

        document_list = doc_session.query(Document) \
                        .filter(Document.batch_number == selected_batch_option.split(" ")[1]).all()
        texts = [doc.content for doc in document_list]
        print(texts[0])

        with st.spinner("Creating your visualizations:"):
            if selected_model != "Not available for documents upload" and selected_model != "BERTopic Wikipedia":
                loaded_model = BERTopic.load(selected_model + "model_safetensors")
                display_visualizations(loaded_model, texts)
            else:
                display_visualizations(None, texts)