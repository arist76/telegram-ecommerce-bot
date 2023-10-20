from pydantic import BaseModel
from typing import ForwardRef
from typing import Optional
import json


class Model:
    def save():
        pass


CategoryRef = ForwardRef("Category")


class Category(BaseModel, Model):
    id: int
    name: Optional[str]
    emoji: Optional[str]
    parent: Optional[CategoryRef]

    @staticmethod
    async def children(parent_id: int = 0):
        pass

    async def grand_parent(id: int):
        pass


class User(BaseModel, Model):
    id: int
    is_bot: Optional[bool]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

    @staticmethod
    async def get_user(user_id: int, payload: list | str = "__all__") -> dict:
        pass

    @staticmethod
    async def exists(user_id) -> bool:
        pass


class Product(BaseModel, Model):
    name: str
    price: Optional[float]
    category: Optional[Category]
    sold: Optional[bool]
