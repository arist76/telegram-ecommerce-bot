from __future__ import annotations
import urllib.parse
from pydantic import BaseModel
from typing import ForwardRef, Optional, List
from datetime import datetime
import httpx
import urllib

# model_backend = os.environ.get("BACKEND_API_HOST")
model_backend = "http://localhost:8000/client/"


class BackendAPIError(Exception):
    pass


CategoryRef = ForwardRef("Category")


class CreateMixin:
    def create(self):

        data = self.model_dump()

        user = self.__class__(data=data)

        res = httpx.post(f"{model_backend}{self.resource_path()}", data=data)

        if res.status_code != 201:
            raise BackendAPIError(
                f"did not create resource, response with status code {res.status_code}"
            )

        return user


class UpdateMixin:
    def update(self):
        pass


class DeleteMixin:
    def delete(self) -> True:
        id = self.model_dump().get("id")

        res = httpx.delete(f"{model_backend}{self.resource_path()}{id}/")

        if res.status_code != 204:
            raise BackendAPIError(
                f"did not create resource, response with status code {res.status_code}"
            )

        return True


class ReadMixin:
    @classmethod
    def read(cls, pk: int | None = None, data: dict | None = None):
        if pk != None:

            if data != None:
                raise ValueError("data must not be provided if pk is optional")

            res = httpx.get(f"{model_backend}{cls.resource_path()}{pk}/")

            if res.status_code != 200:
                raise BackendAPIError(
                    f"error getting resource, status code {res.status_code}"
                )

            data = res.json()
        return data

    @classmethod
    def exists(cls, pk: int):
        res = httpx.head(f"{model_backend}{cls.resource_path()}{pk}/")

        if res.status_code == 200:
            return True
        return False


class ListMixin:
    @classmethod
    def all(cls, *args, **kwargs):
        res = httpx.get(f"{model_backend}{cls.resource_path()}", params=kwargs)

        if res.status_code != 200:
            raise BackendAPIError(
                f"error getting resource, status code {res.status_code}"
            )

        data = res.json()

        prev = urllib.parse.parse_qs(data.get("previous")).get("page", 0)
        next = urllib.parse.parse_qs(data.get("next")).get("page", 2)

        return (
            [cls(data=each) for each in data.get("results")],
            data.get("count"),
            prev,
            next,
        )


class Category(BaseModel, ReadMixin, ListMixin):
    uuid: str
    name: Optional[str] = None
    emoji: Optional[str] = None
    parent: Optional[str] = None
    children: Optional[List[Category]] = None

    def __init__(self, pk: int | None = None, data: dict | None = None, **kwargs):
        if data == None and kwargs:
            data = kwargs

        super().__init__(**self.read(pk=pk, data=data))

    @classmethod
    def resource_path(cls):
        return f"category/"


class User(BaseModel, CreateMixin, DeleteMixin, ReadMixin):
    uuid: str
    id: int
    is_bot: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    date_created: Optional[datetime] = None

    def __init__(self, pk: int | None = None, data: dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    def resource_path(cls):
        return f"user/"


class Product(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    uuid: str
    name: str
    price: Optional[float]
    category: Optional[str]
    sold: Optional[bool]
    images: Optional[list[dict]]

    def __init__(self, pk: int | None = None, data: dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    def resource_path(cls):
        return f"product/"

    @classmethod
    def user_saved_products(cls, user_id) -> list[Product]:
        products, _, _, _ = Product.all(saved_by=user_id)
        return products


class Click(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    id: int
    type: Optional[str]
    name: Optional[str]
    user: Optional[int]

    def __init__(self, pk: int | None = None, data: dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    def resource_path(cls):
        return f"click/"


class Notification(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    id: int
    user: Optional[int]
    category: Optional[int]

    def __init__(self, pk: int | None = None, data: dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    def resource_path(cls):
        return f"notification/"
