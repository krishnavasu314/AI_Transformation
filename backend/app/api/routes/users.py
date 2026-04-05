from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.api.deps import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserView


router = APIRouter()


@router.get("", response_model=list[UserView])
def list_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
) -> list[User]:
    return db.query(User).options(joinedload(User.role)).order_by(User.full_name.asc()).all()
