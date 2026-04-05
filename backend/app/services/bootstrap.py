from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User


def ensure_seed_data() -> None:
    db: Session = SessionLocal()
    try:
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        user_role = db.query(Role).filter(Role.name == "user").first()

        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)
        if not user_role:
            user_role = Role(name="user")
            db.add(user_role)
        db.commit()

        admin_exists = db.query(User).filter(User.username == "admin").first()
        user_exists = db.query(User).filter(User.username == "user1").first()
        if not admin_exists:
            admin_role = db.query(Role).filter(Role.name == "admin").one()
            db.add(
                User(
                    username="admin",
                    full_name="System Admin",
                    email="admin@example.com",
                    hashed_password=hash_password("admin123"),
                    role_id=admin_role.id,
                )
            )
        if not user_exists:
            user_role = db.query(Role).filter(Role.name == "user").one()
            db.add(
                User(
                    username="user1",
                    full_name="Default User",
                    email="user1@example.com",
                    hashed_password=hash_password("user123"),
                    role_id=user_role.id,
                )
            )
        db.commit()
    finally:
        db.close()
