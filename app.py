import streamlit as st

SUPPORTED_FORMATS = ["csv", "txt", "pdf"]


st.title("Topic Modeling and Visualization")

uploaded_files = st.file_uploader(
    "Upload files for topic modeling",
    type=SUPPORTED_FORMATS,
    accept_multiple_files=True,
    label_visibility="collapsed",
)
st.divider()
if uploaded_files:
    with st.columns(3)[1]:
        st.button(
            "Analyze Topics",
            use_container_width=True,
            type="primary",
        )
else:
    st.markdown("_Please upload one or more files for topic analysis._")
