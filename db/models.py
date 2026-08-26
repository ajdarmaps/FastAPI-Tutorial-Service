from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .engine import Base
from datetime import datetime
from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        init=False,
    )

    password: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)

    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default_factory=uuid4,
    )
    __table_args__ = (
        sa.CheckConstraint(
            "length(trim(username)) >= 3",
            name="ck_users_username_min_length",
        ),
    )


class Post(Base):
    __tablename__ = "posts"

    author: Mapped["User"] = relationship(
        back_populates="posts",
        init=False,
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
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        init=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        init=False,
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default_factory=uuid4,
    )
    __table_args__ = (
        sa.Index(
            "ix_posts_author_created_id",
            "author_id",
            "created_at",
            "id",
        ),
    )
