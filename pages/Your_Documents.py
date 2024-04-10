# pages/Your_Documents.py

import streamlit as st
from database import init_db

def display_documents():
    st.title("Your Documents")
    db = init_db("sqlite:///appdatabase.db")
    documents = db.get_documents()  # No batch_number provided

    if documents:
        st.write("Uploaded Documents:")
        # Display documents in a table format
        st.write("Batch Number", "Document Name", "Upload Time")
        for document in documents:
            st.write(document.batch_number, document.filename, document.upload_time)
    else:
        st.write("No documents uploaded yet.")

    # Add button to clear database
    if st.button("Clear Database"):
        db.clear_database()
        st.write("Database cleared successfully.")

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
