import streamlit as st

from .operations import DatabaseOperations


@st.cache_resource(show_spinner="Connecting to database...")
def init_db(db_uri):
    db_operations = DatabaseOperations(db_uri)
    return db_operations
