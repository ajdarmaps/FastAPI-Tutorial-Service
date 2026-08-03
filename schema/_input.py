from pydantic import BaseModel, Field
from typing import Annotated


class UserInput(BaseModel):
    username: str
    password: str


class UpdateUserProfileInput(BaseModel):
    old_username: str
    new_username: str


class DeleteUserAccountInput(BaseModel):
    password: str


class CreatePostInput(BaseModel):
    title: Annotated[
        str,
        Field(min_length=3, max_length=255),
    ]
    content: Annotated[
        str,
        Field(min_length=10, max_length=50000),
    ]


class UpdatePostInput(BaseModel):
    title: Annotated[
        str | None,
        Field(min_length=3, max_length=255),
    ] = None

    content: Annotated[
        str | None,
        Field(min_length=10),
    ] = None