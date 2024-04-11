import pandas as pd
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

    ################# SAVE INDIVIDUAL DOCUMENTS FOR TAB 2 #################

    # TODO: save a single document: maybe don't need this
    def save_document(self, filename, batch_number):
        session = self.Session()
        document = Document(filename=filename, batch_number=batch_number)
        session.add(document)
        session.commit()
        session.close()

    ################# SAVE ZIP FOLDER (DATASET) FOR TAB 1 #################

    # IMPLEMENTATION 1: do not reupload files that are already in the database
    '''
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
    '''

    # IMPLEMENTATION 2: upload duplicate files as long as they are in a new batch
    '''
    def save_documents(self, file_contents, batch_number):
        session = self.Session()
        for filename, content in file_contents.items():
            # Check if the document already exists in the database
            existing_document = session.query(Document).filter_by(filename=filename).first()
            if existing_document:
                # If the document already exists, update its batch number
                existing_document.batch_number = batch_number
            else:
                # If the document does not exist, create a new record
                document = Document(filename=filename, batch_number=batch_number)
                session.add(document)
        session.commit()
        session.close()
    '''

    def save_documents(self, file_contents, batch_number):
        session = self.Session()
        for filename, content in file_contents.items():
            # check if the document already exists in the database
            existing_document = session.query(Document).filter_by(filename=filename).first()
            if existing_document:
                batch_number -= 1
                if isinstance(content, pd.DataFrame):
                    # convert DataFrame to string and update the content
                    content_str = content.to_string(index=False)
                    existing_document.content = content_str
                else:
                    existing_document.content = content
            else:
                # if the document does not exist, create a new record
                if isinstance(content, pd.DataFrame):
                    # convert DataFrame to string and store it as content
                    content_str = content.to_string(index=False)
                    document = Document(filename=filename, batch_number=batch_number, content=content_str)
                else:
                    document = Document(filename=filename, batch_number=batch_number, content=content)
                session.add(document)
        session.commit()
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
        # drop existing table
        Document.__table__.drop(self.engine)
        # recreate the table with the updated schema
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
            return 0  # return 0 if no batches exist
