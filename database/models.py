from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Text, Float

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    batch_number = Column(Integer)
    upload_time = Column(DateTime(timezone=True), default=func.now())
    content = Column(Text) 
    upload_type = Column(String)  # distinguish between 'dataset' upload and 'documents' upload
    topics = Column(String)  # store topics detected
    probabilities = Column(String)  # store corresponding probabilities
    model_names = Column(String)
    path_to_models = Column(String)