import pandas as pd
import streamlit as st
from nlp.topic_modeling import get_pretrained_model, transform_doc_pretrained
from nlp.topic_visualizations import visualize_topics

from database import init_db
from database.models import Document
from sqlalchemy import func

def display_visualizations(model, texts):

    if not model:
        model = get_pretrained_model()

    plot_title = f"Topic Bubbles for BERTopicWikipedia"

    model = get_pretrained_model()

    topic_vis = visualize_topics(model,
                                    topics=None,
                                    top_n_topics=40,
                                    custom_labels=False,
                                    title=plot_title,
                                    width=800,
                                    height=800,
                                    new_document="goalscorer scored goals goals goalkeeper")
    topic_vis.update_layout(
                                    title_font=dict(color="white"),
                                    hoverlabel=dict(bgcolor="black"),
                                    width = 800,
                                    height = 800)
    st.plotly_chart(topic_vis)
    
    # model.visualize_documents(texts)

if __name__ == "__main__":

    st.title("Topic Modeling Visualizations")

    doc_db = init_db("sqlite:///db1.db")
    doc_session = doc_db.Session()

    #model_db = init_db("sqlite:///db1.db")
    #model_session = model_db.Session()

    # TODO: Model selection dropdown

    # Document selection dropdown
    batchnum_list = doc_session.query(Document.batch_number, func.count(Document.batch_number)) \
                             .group_by(Document.batch_number).all()
    batchnum_list = [f"Group {b[0]} ({b[1]} documents)" for b in batchnum_list]
    selected_batch = st.selectbox("Documents to visualize:", batchnum_list)

    if st.button("Visualize documents!", key="visualize_docs_btn"):
        document_list = doc_session.query(Document).filter(Document.batch_number == selected_batch).all()
        display_visualizations(None, document_list)