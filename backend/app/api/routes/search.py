from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.search import SearchHit, SearchRequest, SearchResultSet
from app.services.logging_service import write_audit_log
from app.services.vector_store import knowledge_index


router = APIRouter()


@router.post("", response_model=SearchResultSet)
def search_documents(
    payload: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SearchResultSet:
    results = knowledge_index.search(query=payload.query, top_k=payload.top_k)
    write_audit_log(db, "search", f"Query: {payload.query}", current_user.id)
    return SearchResultSet(
        query=payload.query,
        results=[SearchHit(**item) for item in results],
    )
