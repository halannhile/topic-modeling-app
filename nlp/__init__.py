from streamlit.runtime.uploaded_file_manager import UploadedFile

SUPPORTED_INPUT_FORMATS = ["csv", "txt", "pdf"]


def process_files(uploaded_files: list[UploadedFile]):
    if not uploaded_files:
        raise ValueError("No files uploaded for processing")

    file_contents = {}

    for file in uploaded_files:

        file_extension = file.name.split(".")[-1].lower()
        if file_extension not in SUPPORTED_INPUT_FORMATS:
            raise ValueError(f"Unsupported file format: {file_extension}")

        if file_extension == "txt":
            text = file.read().decode("utf-8")
            file_contents[file.name] = text

        # TODO - Implement file processing for csv and pdf

    return file_contents
