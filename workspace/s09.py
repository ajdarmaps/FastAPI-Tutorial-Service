from pprint import pprint
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

Password = Annotated[str, Field(min_length=5, strict=True)]
Username = Annotated[str, Field(min_length=2, strict=True)]


class User(BaseModel):
    user_name: Username
    pass1: Password
    pass2: Password

    @model_validator(mode="after")
    def check_password_match(self) -> User:
        if self.pass1 != self.pass2:
            raise ValueError("Passwords do not match!")

        return self


u1 = User(user_name="ajdar", pass1="abc@123", pass2="abc@123")

pprint(u1)
