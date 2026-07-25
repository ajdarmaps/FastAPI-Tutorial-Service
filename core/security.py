from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from uuid import UUID
import jwt
from schema.jwt import JWTPayload, JWTResponsePayload
from core.config import settings


class JWTHandler:

    @staticmethod
    def generate(user_id: UUID) -> JWTResponsePayload:
        now = datetime.now(timezone.utc)

        payload = JWTPayload(
            sub=user_id,
            iat=int(now.timestamp()),
            exp=int(
                (
                    now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                ).timestamp()
            ),
        )

        token = jwt.encode(
            payload.model_dump(mode="json"),
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        return JWTResponsePayload(
            access_token=token,
        )

    @staticmethod
    def verify(token: str) -> JWTPayload:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth token not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            token_data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return JWTPayload.model_validate(token_data)
