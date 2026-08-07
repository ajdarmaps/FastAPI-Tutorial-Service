from typing import Annotated

from fastapi import Depends

from schema._input import PaginationInput

PaginationDep = Annotated[
    PaginationInput,
    Depends(),
]