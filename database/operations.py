from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nlp.utils import UploadedDocument

from .models import Base, Document


class DatabaseOperations:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        # create tables
        Base.metadata.create_all(self.engine)

    ################# SAVE INDIVIDUAL DOCUMENTS FOR TAB 1 #################

    # TODO: save a single document: maybe don't need this
    def save_document(self, filename, batch_number, upload_type):
        session = self.Session()
        document = Document(
            filename=filename, batch_number=batch_number, upload_type=upload_type
        )
        session.add(document)
        session.commit()
        session.close()

    ################# SAVE MULTIPLE DOCUMENTS FOR TAB 2 #################

    # IMPLEMENTATION 1: do not reupload files that are already in the database
    """
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
    """

    # IMPLEMENTATION 2: upload duplicate files as long as they are in a new batch
    """
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
    """

    def save_batch_to_db(
        self,
        docs: list[UploadedDocument],
        upload_type: Literal["documents", "dataset"],
        topics,
        probabilities,
        model_names,
        path_to_models,
    ):
        session = self.Session()
        batch_number = self.get_latest_batch_number() + 1 # TODO: not working correctly for zip upload yet

        try:
            for doc in docs:
                # check if the document already exists in the database for the given upload type
                existing_document = (
                    session.query(Document)
                    .filter_by(filename=doc.filename, upload_type=upload_type)
                    .first()
                )
                if existing_document:
                    existing_document.content = doc.content
                else:
                    # if the document does not exist for the given upload type, create a new record
                    content_str = doc.content
                    document = Document(
                        filename=doc.filename,
                        batch_number=batch_number,
                        content=content_str,
                        upload_type=upload_type,
                        topics=topics,
                        probabilities=probabilities,
                        model_names=model_names,
                        path_to_models=path_to_models,
                    )
                    session.add(document)
            session.commit()
            session.close()
            print("Documents saved successfully.")
        except Exception as e:
            session.rollback()
            session.close()
            print(f"Error saving documents: {e}")


    def get_documents(self, batch_number=None):
        session = self.Session()
        if batch_number is None:
            documents = session.query(Document).all()
        else:
            documents = (
                session.query(Document).filter_by(batch_number=batch_number).all()
            )
        session.close()
        return documents

    def get_all_documents(self):
        session = self.Session()
        documents = session.query(
            Document.filename, Document.content, Document.topics, Document.probabilities, Document.model_names, Document.path_to_models
        ).all()
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

    def delete_document(self, document_id):
        session = self.Session()
        try:
            # Get the document by its ID
            document = session.query(Document).filter_by(id=document_id).first()
            if document:
                # Delete the document
                session.delete(document)
                session.commit()
                print(f"Document with ID {document_id} deleted successfully.")
            else:
                print(f"No document found with ID {document_id}.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting document with ID {document_id}: {e}")
        finally:
            session.close()
    
    def delete_batch(self, batch_number):
        session = self.Session()
        try:
            # Delete all documents with the specified batch number
            session.query(Document).filter_by(batch_number=batch_number).delete()
            session.commit()
            print(f"All documents with batch number {batch_number} deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting documents with batch number {batch_number}: {e}")
        finally:
            session.close()

    def get_latest_batch_number(self) -> int:
        session = self.Session()
        latest_batch = (
            session.query(Document).order_by(Document.batch_number.desc()).first()
        )
        session.close()
        if latest_batch:
            # return the batch number of the latest batch
            return latest_batch.batch_number  # type: ignore
        else:
            return 0  # return 0 if no batches exist

    def get_unique_values(self, column_name):
        session = self.Session()
        try:
            unique_values = (
                session.query(getattr(Document, column_name))
                .distinct()
                .all()
            )
            session.close()
            return [value[0] for value in unique_values]
        except Exception as e:
            session.close()
            print(f"Error fetching unique values for {column_name}: {e}")
            return []