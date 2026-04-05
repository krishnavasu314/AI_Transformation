from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, documents, search, tasks, users
from app.core.config import settings
from app.core.database import Base, engine
from app.services.bootstrap import ensure_seed_data
from app.services.vector_store import knowledge_index


app = FastAPI(
    title="Knowledge Work API",
    version="1.0.0",
    description="Backend for document search, task tracking, and role-based access.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_seed_data()
    knowledge_index.load()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
