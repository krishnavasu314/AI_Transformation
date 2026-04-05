from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentView
from app.services.document_service import store_document
from app.services.logging_service import write_audit_log


router = APIRouter()


@router.get("", response_model=list[DocumentView])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Document]:
    return (
        db.query(Document)
        .options(joinedload(Document.uploaded_by).joinedload(User.role))
        .order_by(Document.created_at.desc())
        .all()
    )


@router.post("", response_model=DocumentView, status_code=status.HTTP_201_CREATED)
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
) -> Document:
    document = store_document(db=db, title=title, uploaded_file=file, uploaded_by=admin_user)
    document = (
        db.query(Document)
        .options(joinedload(Document.uploaded_by).joinedload(User.role))
        .filter(Document.id == document.id)
        .one()
    )
    write_audit_log(db, "document_uploaded", f"Uploaded '{document.title}'", admin_user.id)
    return document
