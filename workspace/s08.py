from pydantic import BaseModel, Field, field_validator
from typing import Annotated

Name = Annotated[str, Field(min_length=2, strict=True)]


class Person(BaseModel):
    first_name: Name
    last_name: Name

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        words = value.strip().split()

        if not words:
            raise ValueError("Name is required.")

        if not all(word.isalpha() for word in words):
            raise ValueError(f'"{value}" is not a valid name.')

        return value.strip().capitalize()


p1 = Person(first_name="hamid reza", last_name="ajdar")
print(p1)