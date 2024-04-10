import streamlit as st
from database import init_db

def display_documents():
    st.title("Your Documents")
    db = init_db("sqlite:///topic_modeling.db")
    documents = db.get_documents()

    if documents:
        st.write("Uploaded Documents:")
        for document in documents:
            st.write(f"Filename: {document.filename}, Batch Number: {document.batch_number}")
    else:
        st.write("No documents uploaded yet.")

def main():
    st.set_page_config(
        page_title="Your Documents",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    display_documents()

if __name__ == "__main__":
    main()