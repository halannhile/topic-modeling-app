import pandas as pd
import streamlit as st
from database import init_db

db = init_db('sqlite:///db1.db')

def topic_modeling_results_page():
    st.title("Topic Modeling Results")

    # Fetch data from database
    data = db.get_all_documents()

    # Display data in a table
    st.dataframe(pd.DataFrame(data, columns=["Filename", "Content", "Topic", "Probability"]))
