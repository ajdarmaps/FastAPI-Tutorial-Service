from pydantic import BaseModel
from uuid import UUID


class JWTPayload(BaseModel):
    sub: UUID
    exp: int
    iat: int


class JWTResponsePayload(BaseModel):
    access_token: str
    token_type: str = "Bearer"
