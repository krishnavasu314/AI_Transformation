from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResult
from app.services.auth import login_user
from app.services.logging_service import write_audit_log


router = APIRouter()


@router.post("/login", response_model=LoginResult)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResult:
    token, user = login_user(db, payload.username, payload.password)
    write_audit_log(db, action="login", details=f"{user.username} signed in", user_id=user.id)
    return LoginResult(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.name,
        },
    )
