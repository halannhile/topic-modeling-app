import streamlit as st
from database import init_db
import zipfile
import nlp  # process_zip, SUPPORTED_INPUT_FORMATS, process_files
from nlp.topic_modeling import pretrained_model, transform_doc_pretrained

db = init_db("sqlite:///db1.db")


def analyze_button():
    with st.columns(3)[1]:
        return st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
        )


def main():
    st.set_page_config(
        page_title="Upload Documents",
        page_icon="📤",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    docs_tab, dataset_tab = st.tabs(["Upload Document", "Upload Dataset"])

    with docs_tab:
        st.title("Upload Documents for Topic Analysis")

        # for user to paste input text
        input_text = st.text_area("Paste input text here:", height=200)

        # for user to enter file name
        file_name = st.text_input("Enter file name:", value="text_input.txt")

        uploaded_files = st.file_uploader(
            "Upload files for topic analysis",
            type=nlp.SUPPORTED_INPUT_FORMATS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="document_uploader",
        )

        st.divider()

        if st.button("Analyze Topics", key="analyze_documents_button"):
            if uploaded_files or input_text:
                docs = []
                if input_text:
                    docs = [nlp.UploadedDocument(input_text, file_name)]
                elif uploaded_files:
                    docs: list[nlp.UploadedDocument] = nlp.process_files(uploaded_files)

                for doc in docs:
                    topic, prob, label = transform_doc_pretrained(doc)
                    db.save_batch_to_db(
                        [doc],
                        upload_type="documents",
                        topics=label,
                        probabilities=str(prob),
                    )

                st.success("Topic modeling completed. Results saved to database.")

        else:
            st.markdown("_Please upload one or more files for topic analysis._")

    with dataset_tab:
        st.title("Upload Dataset for Topic Analysis")

        uploaded_zip = st.file_uploader(
            "Upload files for topic modeling",
            type=["zip"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            key="dataset",
        )

        st.divider()

        if uploaded_zip:
            docs = nlp.process_zip(zipfile.ZipFile(uploaded_zip))

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


if __name__ == "__main__":
    main()
