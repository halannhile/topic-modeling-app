import os
import streamlit as st
from database import init_db
import zipfile

from nlp import SUPPORTED_INPUT_FORMATS
from nlp.topic_modeling import (
    get_pretrained_model,
    transform_doc_pretrained,
    train_model,
    train_model_2
)
from nlp.utils import UploadedDocument, process_files, process_zip

import os

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded",
)

db = init_db("sqlite:///db3.db")


inference_tab, training_tab = st.tabs(
    ["Upload Documents for Inference", "Upload Dataset for Training"]
)

with inference_tab:
    st.title("Upload Documents for Inference")

    file_upload_tab, text_input_tab = st.tabs(["Upload Files", "Paste Text"])

    with file_upload_tab:
        uploaded_files = st.file_uploader(
            "Upload files for topic analysis",
            type=SUPPORTED_INPUT_FORMATS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="document_uploader",
        )

    with text_input_tab:
        # for user to paste input text
        input_text = st.text_area("Paste input text here:", height=200)

        # for user to enter file name
        file_name = st.text_input(
            "Enter file name for text input:", value="text_input.txt"
        )

    st.divider()

    if uploaded_files or input_text:
        if st.button("Analyze Topics", key="analyze_documents_button"):
            docs = []
            if input_text:
                docs = [UploadedDocument(input_text, file_name)]
            elif uploaded_files:
                docs: list[UploadedDocument] = process_files(uploaded_files)

            # preload the model (shows spinner)
            get_pretrained_model()

            pbar = st.progress(0.0)
            for i, doc in enumerate(docs):
                pbar.progress(i / len(docs), text=f"Analyzing {doc.filename}...")
                topic, prob, label = transform_doc_pretrained(doc)
                db.save_batch_to_db(
                    [doc],
                    upload_type="documents",
                    topics=label,
                    probabilities=str(prob),
                    model_names="Not available for documents upload",
                    path_to_models="Not available for documents upload",
                )
            pbar.progress(1.0, text="Analysis complete.")

            st.success("Topic modeling completed. Results saved to database.")

    else:
        st.markdown(
            "_Please upload one or more files or enter text for topic analysis._"
        )

################################### IAN'S CODE ###################################

# with training_tab:
#     st.title("Upload Dataset for Training")

#     uploaded_zip = st.file_uploader(
#         "Upload files for topic modeling",
#         type=["zip"],
#         accept_multiple_files=False,
#         label_visibility="collapsed",
#         key="dataset",
#     )

#     st.divider()

#     if uploaded_zip:
#         # cache the documents to avoid unzipping again when the user clicks the button
#         if (
#             "unzip_cache" not in st.session_state
#             or st.session_state["unzip_cache"][0] != uploaded_zip.file_id
#         ):
#             with st.spinner("Unzipping..."):
#                 docs = process_zip(zipfile.ZipFile(uploaded_zip))
#                 st.session_state["unzip_cache"] = (uploaded_zip.file_id, docs)

#         _, docs = st.session_state["unzip_cache"]

#         st.write("Uploaded files:")
#         for doc in docs[:5]:
#             st.write(doc.filename)
#         if len(docs) > 5:
#             st.write(f"and {len(docs) - 5} more files ({len(docs)} total)")

#         default_model_path = os.path.join(os.getcwd(), "trained_model")
#         model_path = st.text_input(
#             "Enter the path to save the trained model:", value=default_model_path
#         )
#         valid_path = os.path.exists(os.path.dirname(model_path))

#         if st.button(
#             "Train Topic Model",
#             disabled=not valid_path,
#             help="Begin training the model",
#         ):
#             with st.spinner("Training model (this may take a while)..."):
#                 train_model(docs, model_path)
#             st.success(f"Topic modeling completed. Model saved to {model_path}.")

#     else:
#         st.markdown(
#             "_Please upload one or more files or paste input text for topic analysis._"
#         )


######################### NHI'S APPROACH: USING TRAIN_MODEL_2() #########################

    # with st.sidebar:
    #     st.title("Settings")
    #     num_clusters = st.number_input("Number of Clusters", min_value=2, step=1, value=5)

    # with training_tab:
    #     st.title("Upload Dataset for Training")

    #     uploaded_zip = st.file_uploader(
    #         "Upload files for topic modeling",
    #         type=["zip"],
    #         accept_multiple_files=False,
    #         label_visibility="collapsed",
    #         key="dataset",
    #     )

    #     st.divider()

    #     if uploaded_zip:
    #         # cache the documents to avoid unzipping again when the user clicks the button
    #         if (
    #             "unzip_cache" not in st.session_state
    #             or st.session_state["unzip_cache"][0] != uploaded_zip.file_id
    #         ):
    #             with st.spinner("Unzipping..."):
    #                 docs = process_zip(zipfile.ZipFile(uploaded_zip))
    #                 st.session_state["unzip_cache"] = (uploaded_zip.file_id, docs)

    #         _, docs = st.session_state["unzip_cache"]

    #         st.write("Uploaded files:")
    #         for doc in docs[:5]:
    #             st.write(doc.filename)
    #         if len(docs) > 5:
    #             st.write(f"and {len(docs) - 5} more files ({len(docs)} total)")

    #         default_model_path = os.path.join(os.getcwd(), "trained_model")
    #         model_path = st.text_input(
    #             "Enter the path to save the trained model:", value=default_model_path
    #         )
    #         valid_path = os.path.exists(os.path.dirname(model_path))

    #         if st.button(
    #             "Train Topic Model",
    #             disabled=not valid_path,
    #             help="Begin training the model",
    #         ):
    #             with st.spinner("Training model (this may take a while)..."):
    #                 train_model(uploaded_zip, model_path, num_clusters)  # Use train_model_2 instead of train_model
    #             st.success(f"Topic modeling completed. Model saved to {model_path}.")

    #     else:
    #         st.markdown(
    #             "_Please upload one or more files or paste input text for topic analysis._"
    #         )

with training_tab:
    st.title("Upload Dataset for Training")

    uploaded_zip = st.file_uploader(
        "Upload files for topic modeling",
        type=["zip"],
        accept_multiple_files=False,
        label_visibility="collapsed",
        key="dataset",
    )

    st.divider()

    if uploaded_zip:
        # cache the documents to avoid unzipping again when the user clicks the button
        if (
            "unzip_cache" not in st.session_state
            or st.session_state["unzip_cache"][0] != uploaded_zip.file_id
        ):
            with st.spinner("Unzipping..."):
                docs = process_zip(zipfile.ZipFile(uploaded_zip))
                st.session_state["unzip_cache"] = (uploaded_zip.file_id, docs)

        _, docs = st.session_state["unzip_cache"]

        st.write("Uploaded files:")
        for doc in docs[:5]:
            st.write(doc.filename)
        if len(docs) > 5:
            st.write(f"and {len(docs) - 5} more files ({len(docs)} total)")

        default_model_path = os.path.join(os.getcwd(), "trained_models\\")
        model_path = st.text_input(
            "Enter the path to save the trained model:", value=default_model_path
        )
        valid_path = os.path.exists(os.path.dirname(model_path))

        if st.button(
            "Train Topic Model",
            disabled=not valid_path,
            help="Begin training the model",
        ):
            num_clusters = st.sidebar.number_input("Number of Clusters", min_value=2, step=1, value=5)
            with st.spinner("Training model (this may take a while)..."):
                train_model(docs, model_path, num_clusters)  # Use train_model instead of train_model_2

            # Save documents and model information to the database
            pbar = st.progress(0.0)
            for i, doc in enumerate(docs):
                pbar.progress(i / len(docs), text=f"Saving document {doc.filename}...")
                db.save_batch_to_db(
                    [doc],
                    upload_type="dataset",
                    topics="",
                    probabilities="",
                    model_names=model_path,  # TODO: saving model path as model_names for now
                    path_to_models=model_path,  # Save model path as path_to_models
                )
            pbar.progress(1.0, text="Documents saved to database.")

            st.success(f"Topic modeling completed. Model and documents saved to database.")

    else:
        st.markdown(
            "_Please upload a zip folder of at least 10 documents for training a topic analysis model._"
        )