from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

Username = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
    ),
]


class UserInput(BaseModel):
    username: Username
    password: str


class UpdateUserProfileInput(BaseModel):
    new_username: Username


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
        Field(min_length=10, max_length=50000),
    ] = None


class PaginationInput(BaseModel):
    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )
