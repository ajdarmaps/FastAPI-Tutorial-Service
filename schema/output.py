from pydantic import BaseModel, ConfigDict
from uuid import UUID


class RegisterOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    id: UUID
