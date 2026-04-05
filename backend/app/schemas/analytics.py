from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    total_documents: int
    total_searches: int
    top_queries: list[dict]
