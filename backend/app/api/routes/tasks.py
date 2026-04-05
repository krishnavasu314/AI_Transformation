from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskView
from app.services.logging_service import write_audit_log


router = APIRouter()


@router.get("", response_model=list[TaskView])
def list_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    assigned_to: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Task]:
    query = db.query(Task).options(joinedload(Task.assigned_to).joinedload(User.role), joinedload(Task.created_by).joinedload(User.role))
    if current_user.role.name != "admin":
        query = query.filter(Task.assigned_to_id == current_user.id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if assigned_to:
        query = query.filter(Task.assigned_to_id == assigned_to)
    return query.order_by(Task.created_at.desc()).all()


@router.post("", response_model=TaskView, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
) -> Task:
    assignee = db.query(User).options(joinedload(User.role)).filter(User.id == payload.assigned_to_id).first()
    if not assignee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
    task = Task(
        title=payload.title,
        description=payload.description,
        assigned_to_id=payload.assigned_to_id,
        created_by_id=admin_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    task = (
        db.query(Task)
        .options(joinedload(Task.assigned_to).joinedload(User.role), joinedload(Task.created_by).joinedload(User.role))
        .filter(Task.id == task.id)
        .one()
    )
    write_audit_log(db, "task_created", f"Assigned '{task.title}' to user {payload.assigned_to_id}", admin_user.id)
    return task


@router.put("/{task_id}", response_model=TaskView)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    task = (
        db.query(Task)
        .options(joinedload(Task.assigned_to).joinedload(User.role), joinedload(Task.created_by).joinedload(User.role))
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if current_user.role.name != "admin" and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this task")
    if payload.status not in {TaskStatus.pending.value, TaskStatus.completed.value}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task status")
    task.status = payload.status
    db.commit()
    db.refresh(task)
    write_audit_log(db, "task_updated", f"Set '{task.title}' to {task.status}", current_user.id)
    return task
