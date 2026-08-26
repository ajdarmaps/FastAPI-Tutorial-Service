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
    author_id: UUID
    author: AuthorOutput
    created_at: datetime
    updated_at: datetime
    

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedPostsOutput(BaseModel):
    items: list[PostOutput]
    meta: PaginationMeta


class AuthorOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
