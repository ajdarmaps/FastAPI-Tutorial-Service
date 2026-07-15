from typing import List

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./orm.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String, unique=True)
    posts: Mapped[List["Post"]] = relationship(back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    content: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")


Base.metadata.create_all(engine)


with Session(engine) as session:
    user = User(
        name="Ali",
        email="ali@example.com",
        posts=[
            Post(title="First Post", content="Hello from SQLAlchemy 2.0"),
            Post(title="Second Post", content="Another post"),
        ],
    )

    session.add(user)
    session.commit()


with Session(engine) as session:
    stmt = select(User).where(User.name == "Ali")
    result = session.execute(stmt)
    user = result.scalar_one()

    print(user.name, user.email)

    for post in user.posts:
        print(post.title, post.content)
