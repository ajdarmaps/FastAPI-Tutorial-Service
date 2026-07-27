from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db
