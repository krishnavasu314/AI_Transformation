from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserView


class DocumentView(BaseModel):
    id: int
    title: str
    filename: str
    content_preview: str
    chunk_count: int
    created_at: datetime
    uploaded_by: UserView

    model_config = ConfigDict(from_attributes=True)
