# pages/Upload_Documents.py

import streamlit as st
from database import init_db
import zipfile
import nlp  # process_zip, SUPPORTED_INPUT_FORMATS, process_files

# Initialize database connection
db = init_db('sqlite:///mydatabase.db')


def analyze_button(key):
    with st.columns(3)[1]:
        return st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
            key=key
        )

def main():
    st.set_page_config(
        page_title="Upload Documents",
        page_icon="📤",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    tab1, tab2 = st.tabs(["Upload Dataset", "Upload Document"])

    with tab1:
        st.title("Upload Dataset for Topic Analysis")

        uploaded_zip = st.file_uploader(
            "Upload files for topic modeling",
            type=["zip"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            key="dataset",
        )
        st.divider()
        if uploaded_zip:
            zf = zipfile.ZipFile(uploaded_zip)
            file_contents = nlp.process_zip(zf)
            db.save_documents(file_contents)
            if analyze_button("analyze_button_tab1"):
                pass
            else:
                st.markdown("_Please upload one or more files for topic analysis._")

    with tab2:
        st.title("Upload Documents for Topic Analysis")

        uploaded_files = st.file_uploader(
            "Upload files for topic modeling",
            type=nlp.SUPPORTED_INPUT_FORMATS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="document",
        )

        if uploaded_files:
            st.write("Uploaded Files:")
            for uploaded_file in uploaded_files:
                st.write(uploaded_file.name)

        if uploaded_files:
            if analyze_button("analyze_button_tab2"):
                file_contents = nlp.process_files(uploaded_files)
                db.save_documents(file_contents)
            else:
                st.markdown("_Please upload one or more files for topic analysis._")

    # Upload button outside tabs
    st.button("Upload", key="upload_button")



if __name__ == "__main__":
    main()
