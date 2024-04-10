# database/operations.py

from .models import Base, Document
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

class DatabaseOperations:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        # create tables
        Base.metadata.create_all(self.engine)

    # save a single document
    def save_document(self, filename, batch_number):
        session = self.Session()
        document = Document(filename=filename, batch_number=batch_number)
        session.add(document)
        session.commit()
        session.close()

    # save multiple documents
    def save_documents(self, file_contents, batch_number):
        session = self.Session()
        for filename, text in file_contents.items():
            # Check if document with same filename already exists
            existing_document = session.query(Document).filter_by(filename=filename).first()
            if existing_document:
                # Update existing document with new batch number
                # existing_document.batch_number = batch_number
                # decrement batch_number and do nothing
                batch_number -= 1
            else:
                # Create new document entry
                document = Document(filename=filename, batch_number=batch_number)
                session.add(document)
        
        # Commit changes to database
        try:
            session.commit()
        except IntegrityError:
            # Rollback changes in case of error
            session.rollback()
        finally:
            session.close()

    def get_documents(self, batch_number=None):
        session = self.Session()
        if batch_number is None:
            documents = session.query(Document).all()
        else:
            documents = session.query(Document).filter_by(batch_number=batch_number).all()
        session.close()
        return documents

    def clear_database(self):
        session = self.Session()
        # Drop existing table
        Document.__table__.drop(self.engine)
        # Recreate the table with the updated schema
        Base.metadata.create_all(self.engine)
        session.commit()
        session.close()

    def get_latest_batch_number(self):
        session = self.Session()
        latest_batch = session.query(Document).order_by(Document.batch_number.desc()).first()
        session.close()
        if latest_batch:
            return latest_batch.batch_number
        else:
            return 0  # Return 0 if no batches exist
