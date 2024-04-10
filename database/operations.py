from .models import Base, Document
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseOperations:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        # create tables
        Base.metadata.create_all(self.engine)

    def save_document(self, filename, batch_number):
        session = self.Session()
        document = Document(filename=filename, batch_number=batch_number)
        session.add(document)
        session.commit()
        session.close()

    def save_documents(self, file_contents, batch_number):
        session = self.Session()
        for filename, text in file_contents.items():
            document = Document(filename=filename, batch_number=batch_number)
            session.add(document)
        session.commit()
        session.close()

    def get_documents(self):
        session = self.Session()
        documents = session.query(Document).all()
        session.close()
        return documents
