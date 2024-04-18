import pandas as pd
import streamlit as st
from database import init_db


def display_documents():
    st.title("Topic Modeling Results")

    db = init_db("sqlite:///db3.db")

    # fetch all documents from the database
    documents = db.get_all_documents()

    df = pd.DataFrame(
        documents, columns=["Filename", "Content", "Topic", "Probability"]
    )

    st.table(df)


if __name__ == "__main__":
    display_documents()
