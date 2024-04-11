import pandas as pd
import streamlit as st
from database import init_db


def display_documents():
    st.title("Your Documents")
    db = init_db("sqlite:///db1.db")
    documents = db.get_documents()  # no batch_number provided

    if documents:
        st.write("Uploaded Documents:")
        data = []
        for document in documents:
            data.append(
                [
                    document.batch_number,
                    document.filename,
                    document.upload_time,
                    document.upload_type,
                    document.content,
                    document.topics,
                    document.probabilities,
                ]
            )

        df = pd.DataFrame(
            data,
            columns=[
                "Batch Number",
                "File Name",
                "Time Uploaded",
                "Upload Type",
                "File Content",
                "Topics",
                "Probability",
            ],
        )

        # display the DataFrame in a table
        st.table(df)

        with st.popover("Clear Database"):
            st.write("Are you sure you want to clear all documents from the database?")
            if st.button("Yes, clear the database"):
                db.clear_database()
                st.rerun()
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
