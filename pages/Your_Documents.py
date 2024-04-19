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
db = init_db()
l, r, _ = st.columns([1, 1, 4])
with l:
    page_number = st.number_input("Page number:", min_value=1, step=1)
    if page_number is None:
        page_number = 1
    page_number = int(page_number)
    with st.popover("Delete Documents", use_container_width=True):
        individual, batch, clear = st.tabs(
            ["Delete Individual Document", "Delete Batch", "Clear Database"]
        )

        with individual:
            # Input box for ID of document to delete
            delete_id = st.number_input(
                "Enter the ID of the document you want to delete:", min_value=1, step=1
            )

            if st.button("Delete Document"):
                if delete_id:
                    db.delete_document(delete_id)
                    st.write(
                        f"Document with ID {delete_id} deleted successfully. Refresh the page to see changes."
                    )
                else:
                    st.warning("Please enter a valid ID.")

        with batch:
            # Dropdown menu for selecting batch number to delete
            batches = db.get_all_batches()
            batch_number_to_delete = st.selectbox(
                "Select Batch Number to Delete:", batches, index=None
            )

            if st.button("Delete Batch"):
                if batch_number_to_delete:
                    db.delete_batch(batch_number_to_delete)
                    st.write(
                        f"All documents with batch number {batch_number_to_delete} deleted successfully. . Refresh the page to see changes."
                    )
                else:
                    st.warning("Please select a valid batch number.")
        with clear:
            st.write("Are you sure you want to clear all documents from the database?")
            if st.button("Yes, clear the database"):
                db.clear_database()
                st.rerun()
with r:
    n_results = st.selectbox("Results per page:", [10, 20, 50, 100, 200], index=1)
    if n_results is None:
        n_results = 10
    if st.button("Refresh Database", use_container_width=True):
        st.rerun()

documents = db.get_documents(
    batch_number=None, limit=n_results, offset=(page_number - 1) * n_results
)

if documents:
    data = []
    for document in documents:
        data.append(
            [
                document.id,
                document.batch_number,
                document.filename,
                document.upload_time,
                document.upload_type,
                document.content[:100] + ("..." if len(document.content) > 100 else ""),
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Batch",
            "File Name",
            "Time Uploaded",
            "Upload Type",
            "File Content",
        ],
    )

    # https://discuss.streamlit.io/t/st-dataframe-controlling-the-height-threshold-for-scolling/31769/5
    st.dataframe(
        df, use_container_width=True, hide_index=True, height=(n_results + 1) * 35 + 3
    )
else:
    st.write("No documents found.")
