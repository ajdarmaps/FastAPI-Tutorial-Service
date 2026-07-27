from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .engine import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
    )
    password: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default_factory=uuid4,
    )


class Post(Base):
    __tablename__ = "posts"

    author: Mapped["User"] = relationship(
        back_populates="posts",
    )

    title: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        sa.Text(),
        nullable=False,
    )

    author_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default_factory=uuid4,
    )
