from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.engine import Base, engine
from routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users")
