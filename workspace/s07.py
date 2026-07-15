from enum import Enum
from pprint import pprint
from typing import Annotated

from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Size(Enum):
    small = "small"
    medium = "medium"
    large = "large"


class TShirt(BaseModel):
    brand: Annotated[str, Field(min_length=2, strict=True)]
    size: Size
    quantity: Annotated[int, Field(ge=1, strict=True)] = 1
    id: UUID
    price: Annotated[int, Field(ge=1, strict=True)]


t1 = TShirt(
    brand="Capa",
    size=Size.medium,
    quantity=1,
    id=uuid4(),
    price=100,
)

pprint(t1.model_dump())
