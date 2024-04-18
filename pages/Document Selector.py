import pandas as pd
import streamlit as st
from database import DatabaseOperations

def display_documents():
    st.title("Topic Modeling Results")

    db = DatabaseOperations("sqlite:///db3.db")

    # fetch all unique values for upload_type, batch_number, model_names, and path_to_models
    upload_types = db.get_unique_values("upload_type")
    batch_numbers = db.get_unique_values("batch_number")
    model_names = db.get_unique_values("model_names")
    path_to_models = db.get_unique_values("path_to_models")

    # Create dropdown menus for user selection
    selected_upload_type = st.selectbox("Select Upload Type", upload_types)
    selected_batch_number = st.selectbox("Select Batch Number", batch_numbers)
    if selected_upload_type == "dataset":
        selected_model_name = st.selectbox("Select Model Name", model_names)
        selected_path_to_model = st.selectbox("Select Path to Model", path_to_models)

    # Fetch documents based on user selection
    if st.button("Fetch Documents"):
        documents = db.get_documents_by_filters(
            upload_type=selected_upload_type,
            batch_number=selected_batch_number,
            model_names=selected_model_name if selected_upload_type == "dataset" else None,
            path_to_models=selected_path_to_model if selected_upload_type == "dataset" else None,
        )

        print("documents: ", documents)
        print("Number of documents:", len(documents))
        print("First document:", documents[0] if documents else None)

        if documents:
            df = pd.DataFrame(
                documents, 
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
                ]
            )
            st.table(df)
        else:
            st.write("No documents found with the selected filters.")

if __name__ == "__main__":
    display_documents()
