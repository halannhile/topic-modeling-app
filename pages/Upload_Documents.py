import streamlit as st
from database import init_db
import zipfile
import nlp  # process_zip, SUPPORTED_INPUT_FORMATS, process_files
from bertopic import BERTopic

db = init_db('sqlite:///db1.db')

# this part makes it take some time to launch the Upload Documents page
topic_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")

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

    tab1, tab2 = st.tabs(["Upload Dataset", "Upload Document"])


    with tab1:
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
            with zipfile.ZipFile(uploaded_zip, "r") as zf:
                file_names = zf.namelist()
                st.write("Uploaded files:")
                for file_name in file_names:
                    st.write(file_name)

            if st.button("Upload Dataset", key="upload_button_1"):
                with zipfile.ZipFile(uploaded_zip, "r") as zf:
                    file_contents = nlp.process_zip(zf)
                    current_batch_number = db.get_latest_batch_number() + 1
                    db.save_documents(file_contents, current_batch_number, upload_type='dataset')
                if st.button("Analyze Topics"):
                    # hide the uploaded files section and the Upload Dataset button
                    st.text("Analyzing topics...")

        else:
            st.markdown("_Please upload one or more files for topic analysis._")


    with tab2:
        st.title("Upload Documents for Topic Analysis")

        uploaded_files = st.file_uploader(
            "Upload files for topic modeling",
            type=nlp.SUPPORTED_INPUT_FORMATS,
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="document",
        )

        st.divider()
        if uploaded_files:
            if st.button("Analyze Topics", key="analyze_topics_2"):
                print("Analyze Topics button clicked")
                print("Upload Files button clicked")
                current_batch_number = db.get_latest_batch_number() + 1
                file_contents = nlp.process_files(uploaded_files, upload_type='documents')
                print("file_contents:", file_contents)  # print file_contents to the console

                for filename, content in file_contents.items():
                    print("filename: ", filename)
                    print("content: ", content)
                    topic, prob = topic_model.transform(str(content))
                    print("topic, prob: ", [topic, prob])
                    topic_label = topic_model.topic_labels_[topic[0]]
                    probabilities_str = str(prob)

                    db.save_documents({filename: content}, current_batch_number, upload_type='documents', topics=topic_label, probabilities=probabilities_str)
                    
                st.success("Topic modeling completed. Results saved to database.")

        else:
            st.markdown("_Please upload one or more files for topic analysis._")


if __name__ == "__main__":
    main()