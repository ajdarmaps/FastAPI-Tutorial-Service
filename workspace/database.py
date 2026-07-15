from typing import Optional
from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    relationship,
)
from sqlalchemy.sql import select


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30))
    full_name: Mapped[Optional[str]]
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id},email_address={self.name},user_id={self.full_name})"


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id},email_address={self.email_address},user_id={self.user_id})"


SQLALCHEMY_DATABASE_URL = "sqlite:///./mytestdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
Base.metadata.create_all(engine)


Session = sessionmaker(engine, expire_on_commit=False)

with Session() as session:
    stmt = select(User).where(User.id == 1)
    user = session.execute(stmt).scalar()

    print(user)
    print(user.addresses)
