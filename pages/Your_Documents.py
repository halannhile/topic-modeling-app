import streamlit as st
from database import init_db

def display_documents():
    st.title("Your Documents")
    db = init_db("sqlite:///appdatabase2.db")
    documents = db.get_documents()  # no batch_number provided

    if documents:
        st.write("Uploaded Documents:")
        data = []
        for document in documents:
            data.append([document.batch_number, document.filename, document.upload_time, document.upload_type, document.content])

        data_with_header = [["Batch Number", "File Name", "Time Uploaded", "Upload Type", "File Content"]] + data

        st.table(data_with_header)
    else:
        st.write("No documents uploaded yet.")

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
