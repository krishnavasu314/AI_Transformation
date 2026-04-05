from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserView


class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to_id: int


class TaskUpdate(BaseModel):
    status: str


class TaskView(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    assigned_to: UserView
    created_by: UserView

    model_config = ConfigDict(from_attributes=True)
