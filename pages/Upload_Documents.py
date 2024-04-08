import streamlit as st
import nlp
import zipfile

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded",
)

def analyze_button():
    with st.columns(3)[1]:
        return st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
        )

tab1, tab2 = st.tabs(["Upload Dataset", "Upload Document"])

with tab1:
    st.title("Upload Dataset for Topic Analysis")

    uploaded_zip = st.file_uploader(
        "Upload files for topic modeling",
        type=["zip"],
        accept_multiple_files=False,
        label_visibility="collapsed",
        key="dataset"
    )
    st.divider()
    if uploaded_zip and analyze_button():
        zf = zipfile.ZipFile(uploaded_zip)
        nlp.process_zip(zf)
    else:
        st.markdown("_Please upload one or more files for topic analysis._")

with tab2:
    st.title("Upload Documents for Topic Analysis")

    uploaded_files = st.file_uploader(
        "Upload files for topic modeling",
        type=nlp.SUPPORTED_INPUT_FORMATS,
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="document"
    )
    st.divider()
    if uploaded_files and analyze_button():
        nlp.process_files(uploaded_files)
    else:
        st.markdown("_Please upload one or more files for topic analysis._")