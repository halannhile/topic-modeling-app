import streamlit as st
import pandas as pd
from database import init_db

st.set_page_config(
    page_title="Your Documents",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Your Documents")
db = init_db("sqlite:///db2.db")
documents = db.get_documents()  # no batch_number provided

if documents:
    st.write("Uploaded Documents:")
    data = []
    for document in documents:
        data.append(
            [
                document.id,
                document.batch_number,
                document.filename,
                document.upload_time,
                document.upload_type,
                document.content[:100] + ('...' if len(document.filename) > 100 else ''),
                document.topics,
                document.probabilities,
                document.model_names,
                document.path_to_models,
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Batch Number",
            "File Name",
            "Time Uploaded",
            "Upload Type",
            "File Content",
            "Topics",
            "Probability",
            "Model Names",
            "Path To Models",
        ],
    )

    # Display the DataFrame in a table
    st.table(df)

    # Input box for ID of document to delete
    delete_id = st.number_input(
        "Enter the ID of the document you want to delete:", min_value=1, step=1
    )

    if st.button("Delete Document"):
        if delete_id:
            db.delete_document(delete_id)
            st.write(f"Document with ID {delete_id} deleted successfully.")
        else:
            st.warning("Please enter a valid ID.")

    # Dropdown menu for selecting batch number to delete
    batch_number_to_delete = st.selectbox(
        "Select Batch Number to Delete:", sorted(set(df["Batch Number"]))
    )

    if st.button("Delete Batch"):
        if batch_number_to_delete:
            db.delete_batch(batch_number_to_delete)
            st.write(f"All documents with batch number {batch_number_to_delete} deleted successfully.")
        else:
            st.warning("Please select a valid batch number.")

    with st.popover("Clear Database"):
        st.write("Are you sure you want to clear all documents from the database?")
        if st.button("Yes, clear the database"):
            db.clear_database()
            st.rerun()
else:
    st.write("No documents uploaded yet.")

if st.button("Refresh Database"):
    st.rerun()
