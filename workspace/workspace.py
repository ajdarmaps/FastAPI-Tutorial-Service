from pydantic import BaseModel, ValidationError, Field, ConfigDict
from pydantic.alias_generators import to_camel

from typing import List, Optional
from datetime import date
from pprint import pprint

# class Job(BaseModel):
#     title: str
#     salary: int


# class Person(BaseModel):
#     name: str
#     job: Job
#     birth_date: date


# p1 = Person(
#     name="Hamid",
#     job=Job(title="Developer", salary=100_000),
#     birth_date="1977-10-09",
# )
# pprint(p1)
# print(p1.birth_date.month)


# class TreeNode(BaseModel):
#     value: int
#     children: Optional[List["TreeNode"]] = []

#     def add_child(self, child: "TreeNode") -> None:
#         self.children.append(child)


# root = TreeNode(value=5)
# first_child = TreeNode(value=12)
# second_child = TreeNode(value=7)
# root.add_child(first_child)
# root.add_child(second_child)


# pprint(root)
# pprint(first_child)


class Check(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="allow"
    )
    student_name: str
    age: int
    is_active: bool
    phone: List[str]


data = {
    "student_name": "Hamid",
    "age": 48,
    "is_active": True,
    "phone": ["09121781652", "09124393413"],
    "gpa": 19.8,
}


data_json = """{
    "studentName": "Hamid",
    "age": 48,
    "isActive": true,
    "phone": ["09121781652", "09124393413"],
    "gpa": 19.8
}"""

try:
    # s1 = Check(**data)
    s1 = Check.model_validate(data)
    s2 = Check.model_validate_json(data_json)
    pprint(s1)
    pprint(s2)
except ValidationError as ex:
    pprint(ex)
