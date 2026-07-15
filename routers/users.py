from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.engine import get_db
from operations.users import UsersOperation
from schema._input import RegisterInput

router = APIRouter()


@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: RegisterInput = Body(),
):
    user = await UsersOperation(db_session).create(
        username=data.username, password=data.password
    )
    return user


@router.post("/login")
async def login(): ...


@router.get("/")
async def get_user_profile(): ...


@router.put("/{id}")
async def update_user_profile(): ...
