import os
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document
from app.models.user import User
from app.services.vector_store import knowledge_index
from app.utils.text import split_into_passages


def store_document(db: Session, title: str, uploaded_file: UploadFile, uploaded_by: User) -> Document:
    if not uploaded_file.filename or not uploaded_file.filename.endswith(".txt"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .txt files are supported")

    Path(settings.documents_dir).mkdir(parents=True, exist_ok=True)
    target_path = Path(settings.documents_dir) / uploaded_file.filename
    file_bytes = uploaded_file.file.read()
    text = file_bytes.decode("utf-8")
    target_path.write_text(text, encoding="utf-8")

    chunks = split_into_passages(text)
    document = Document(
        title=title,
        filename=uploaded_file.filename,
        file_path=os.fspath(target_path),
        content_preview=text[:300],
        uploaded_by_id=uploaded_by.id,
        chunk_count=len(chunks),
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    knowledge_index.add_document(document_id=document.id, title=document.title, chunks=chunks)
    return document
