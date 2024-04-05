from sqlalchemy import Column, Integer, String
from .main import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    transcript = Column(String)

    def __repr__(self):
        return f"<Document(file_name='{self.file_name}', transcript='{self.transcript}')>"
