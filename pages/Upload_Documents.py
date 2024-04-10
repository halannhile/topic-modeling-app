import streamlit as st
from database import init_db
import zipfile
import nlp # process_zip, SUPPORTED_INPUT_FORMATS, process_files

# initialize database connection
db = init_db('sqlite:///mydatabase.db')

def analyze_button():
    with st.columns(3)[1]:
        return st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
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
        if uploaded_zip and analyze_button():
            zf = zipfile.ZipFile(uploaded_zip)
            nlp.process_zip(zf)
            # let's assume process_zip returns file_contents
            file_contents = nlp.process_zip(zf)
        else:
            st.markdown("_Please upload one or more files for topic analysis._")
            file_contents = {}  # initialize file_contents as an empty dictionary
        
        if st.button("Upload Dataset To Your Database"):
            db.save_documents(file_contents, batch_number=1)  # TODO: increment batch number

    with tab2:
        st.title("Upload Documents for Topic Analysis")

        uploaded_files = st.file_uploader(
            "Upload files for topic modeling",
            type=nlp.SUPPORTED_INPUT_FORMATS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="document",
        )
        st.divider()
        if uploaded_files and analyze_button():
            # process uploaded files and save to database
            file_contents = nlp.process_files(uploaded_files)
            for filename, text in file_contents.items():
                db.save_document(filename, batch_number=2) # TODO: increment batch number 
        else:
            st.markdown("_Please upload one or more files for topic analysis._")
            file_contents = {}
        
        if st.button("Upload Documents To Your Database"):
            db.save_documents(file_contents, batch_number=2) # TODO: increment batch number

if __name__ == "__main__":
    main()
