from turtle import up
from streamlit.runtime.uploaded_file_manager import UploadedFile

SUPPORTED_INPUT_FORMATS = ["csv", "txt", "pdf"]


def process_files(uploaded_files: list[UploadedFile]):
    if not uploaded_files:
        raise ValueError("No files uploaded for processing")

    for file in uploaded_files:
        if file.type not in SUPPORTED_INPUT_FORMATS:
            raise ValueError(f"Unsupported file format: {file.type}")

        # TODO - Implement file processing
