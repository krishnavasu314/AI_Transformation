from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


def write_audit_log(db: Session, action: str, details: str, user_id: int | None = None) -> None:
    db.add(ActivityLog(action=action, details=details, user_id=user_id))
    db.commit()
