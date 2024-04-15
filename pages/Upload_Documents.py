import streamlit as st
from database import init_db
import zipfile

from nlp import SUPPORTED_INPUT_FORMATS
from nlp.topic_modeling import get_pretrained_model, transform_doc_pretrained
from nlp.utils import UploadedDocument, process_files, process_zip


st.set_page_config(
    page_title="Upload Documents",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded",
)

db = init_db("sqlite:///db1.db")


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
                )
            pbar.progress(1.0, text="Analysis complete.")

            st.success("Topic modeling completed. Results saved to database.")

    else:
        st.markdown(
            "_Please upload one or more files or enter text for topic analysis._"
        )

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
        docs = process_zip(zipfile.ZipFile(uploaded_zip))

        st.write("Uploaded files:")
        for doc in docs:
            st.write(doc.filename)

        if st.button("Upload Dataset", key="upload_button_1"):

            if st.button(
                "Train Topic Model", disabled=True, help="Not yet implemented"
            ):
                # TODO - implement model training
                # train model first, then analyze topics and save docs to database
                # don't forget to increment batch number!
                pass

    else:
        st.markdown(
            "_Please upload one or more files or paste input text for topic analysis._"
        )
