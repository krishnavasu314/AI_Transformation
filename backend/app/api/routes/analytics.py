from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.activity_log import ActivityLog
from app.models.document import Document
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.analytics import DashboardStats


router = APIRouter()


@router.get("", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardStats:
    task_query = db.query(Task)
    if current_user.role.name != "admin":
        task_query = task_query.filter(Task.assigned_to_id == current_user.id)

    total_tasks = task_query.count()
    completed_tasks = task_query.filter(Task.status == TaskStatus.completed.value).count()
    pending_tasks = task_query.filter(Task.status == TaskStatus.pending.value).count()
    total_documents = db.query(Document).count()
    search_query = db.query(ActivityLog).filter(ActivityLog.action == "search")
    if current_user.role.name != "admin":
        search_query = search_query.filter(ActivityLog.user_id == current_user.id)
    total_searches = search_query.count()
    top_queries_raw = (
        search_query.with_entities(ActivityLog.details, func.count(ActivityLog.id).label("count"))
        .group_by(ActivityLog.details)
        .order_by(func.count(ActivityLog.id).desc())
        .limit(5)
        .all()
    )
    top_queries = [{"query": item.details.replace("Query: ", ""), "count": item.count} for item in top_queries_raw]

    return DashboardStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        total_documents=total_documents,
        total_searches=total_searches,
        top_queries=top_queries,
    )
