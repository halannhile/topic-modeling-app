import streamlit as st
import nlp


st.title("Topic Modeling and Visualization")

uploaded_files = st.file_uploader(
    "Upload files for topic modeling",
    type=nlp.SUPPORTED_INPUT_FORMATS,
    accept_multiple_files=True,
    label_visibility="collapsed",
)
st.divider()
if uploaded_files:
    with st.columns(3)[1]:
        if st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
        ):
            nlp.process_files(uploaded_files)
else:
    st.markdown("_Please upload one or more files for topic analysis._")
