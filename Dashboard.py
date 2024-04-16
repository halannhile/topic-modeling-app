import streamlit as st

st.set_page_config(
    page_title="Topic Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Topic Visualization Dashboard")

topics_area, documents_area = st.columns(2)


with topics_area:
    st.header("Topics")
    st.markdown("_No topics to display._")

with documents_area:
    st.header("Documents")
    st.markdown("_No documents to display._")
