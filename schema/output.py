from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str


class PostOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
