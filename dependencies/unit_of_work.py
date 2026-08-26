from typing import Annotated

from fastapi import Depends

from dependencies.database import DbSession
from unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork


def get_unit_of_work(
    db_session: DbSession,
) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(db_session)


UnitOfWorkDep = Annotated[
    SQLAlchemyUnitOfWork,
    Depends(get_unit_of_work),
]