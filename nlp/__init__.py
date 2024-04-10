from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tempfile
from zipfile import ZipFile
import pandas as pd
import textract

SUPPORTED_INPUT_FORMATS = ["csv", "txt", "pdf", "docx"]

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
        elif file_extension == "csv":
            dataframe = pd.read_csv(file)
            # Concatenate all columns' values to create the text content
            text = ' '.join(dataframe.apply(lambda x: ' '.join(x.astype(str)), axis=1))
            file_contents[file.name] = text
        elif file_extension == "pdf":
            text = textract.process(file.getvalue()).decode("utf-8")
            file_contents[file.name] = text
        elif file_extension == "docx":
            text = textract.process(file.getvalue()).decode("utf-8")
            file_contents[file.name] = text

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
