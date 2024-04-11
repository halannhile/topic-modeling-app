from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tempfile
from zipfile import ZipFile
import pandas as pd
import textract
import docx

SUPPORTED_INPUT_FORMATS = ["csv", "txt", "pdf", "docx"]


def process_files(uploaded_files: list[UploadedFile], upload_type: str):
    if not uploaded_files:
        raise ValueError("No files uploaded for processing")

    file_contents = {}

    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension not in SUPPORTED_INPUT_FORMATS:
            raise ValueError(f"Unsupported file format: {file_extension}")

        if file_extension == "txt":
            text = uploaded_file.read().decode("utf-8")
            file_contents[uploaded_file.name] = text
        elif file_extension == "csv":
            dataframe = pd.read_csv(uploaded_file)
            file_contents[uploaded_file.name] = dataframe
        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            file_contents[uploaded_file.name] = text
        # TODO: parse pdf

    return file_contents

def process_zip(uploaded_zip: ZipFile):
    if not uploaded_zip:
        raise ValueError("No zipfile uploaded for processing")

    file_contents = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        uploaded_zip.extractall(temp_dir)
        for filename in Path(temp_dir).rglob("*.*"):
            file_extension = filename.suffix.lower()[1:]  # Remove leading dot
            if file_extension in SUPPORTED_INPUT_FORMATS:
                if file_extension == "txt":
                    with open(filename, "r", encoding="utf-8") as file:
                        file_contents[filename.name] = file.read()
                elif file_extension == "csv":
                    dataframe = pd.read_csv(filename)
                    file_contents[filename.name] = dataframe
                # TODO: reimplement PDF processing
                # elif file_extension == "pdf":
                #     text = textract.process(str(filename)).decode("utf-8")
                #     file_contents[filename.name] = text
                elif file_extension == "docx":
                    text = textract.process(str(filename)).decode("utf-8")
                    file_contents[filename.name] = text


    return file_contents
