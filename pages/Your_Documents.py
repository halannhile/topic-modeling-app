import streamlit as st
from database import init_db

def display_documents():
    st.title("Your Documents")
    db = init_db("sqlite:///app-database.db")
    documents = db.get_documents()  # no batch_number provided

    if documents:
        st.write("Uploaded Documents:")
        data = []
        for document in documents:
            # extract content from DataFrame (for csv files)
            content = document.content
            if hasattr(content, 'values'):
                content = content.values[0][0]  # TODO: debug this: assuming content is stored in the first cell
            data.append([document.batch_number, document.filename, document.upload_time, content])

        # TODO: figure out way to display headers instead of this method: specify column names as first row of data
        data_with_header = [["Batch Number", "File Name", "Time Uploaded", "File Content"]] + data

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
