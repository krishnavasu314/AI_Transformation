from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchHit(BaseModel):
    document_id: int
    document_title: str
    chunk_text: str
    score: float


class SearchResultSet(BaseModel):
    query: str
    results: list[SearchHit]
