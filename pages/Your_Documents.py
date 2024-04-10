import streamlit as st
from database import init_db

# Initialize database connection
db = init_db('sqlite:///mydatabase.db')

def display_documents():
    documents = db.get_documents()
    if documents:
        st.write("Uploaded Documents:")
        for document in documents:
            st.write(f"Filename: {document.filename}, Batch Number: {document.batch_number}")
            # Add preview button here if needed
    else:
        st.write("No documents uploaded yet.")

def main():
    st.title("Your Documents")
    display_documents()

if __name__ == "__main__":
    main()
