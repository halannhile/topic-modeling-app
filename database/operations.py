from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Document

class DatabaseOperations:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_documents(self, file_contents, batch_number):
        session = self.Session()
        try:
            for filename, text in file_contents.items():
                document = Document(filename=filename, batch_number=batch_number)
                session.add(document)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()