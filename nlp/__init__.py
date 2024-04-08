from streamlit.runtime.uploaded_file_manager import UploadedFile
import tempfile
from pathlib import Path

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

def process_zip(uploaded_zip: list[UploadedFile]):
    if not uploaded_zip:
        raise ValueError("No zipfile uploaded for processing")

    file_contents = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        uploaded_zip.extractall(temp_dir)
        for filename in Path(temp_dir).rglob('*.txt'):
            with open(filename, 'r', encoding='utf-8') as file:
                file_contents[filename.name] = file.read()

    return file_contents
