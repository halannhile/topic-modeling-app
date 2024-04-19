import streamlit as st

from .operations import DatabaseOperations

DB_URI = "sqlite:///documents.db"


@st.cache_resource(show_spinner="Connecting to database...")
def init_db():
    db_operations = DatabaseOperations(DB_URI)
    return db_operations
