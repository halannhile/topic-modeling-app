from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Document, Base

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/data.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        content = await file.read()
        # TODO: implement transcript creation
        transcript = "this is a dummy transcript"
        db_doc = Document(file_name=file.filename, transcript=transcript)
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        return {"file_name": file.filename, "transcript": transcript}
    finally:
        db.close()

@app.get("/documents/{document_id}")
async def read_document(document_id: int):
    db = SessionLocal()
    try:
        db_doc = db.query(Document).filter(Document.id == document_id).first()
        if db_doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return db_doc
    finally:
        db.close()
