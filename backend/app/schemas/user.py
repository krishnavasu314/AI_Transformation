from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoleView(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserView(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    created_at: datetime
    role: RoleView

    model_config = ConfigDict(from_attributes=True)
