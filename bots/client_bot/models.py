from __future__ import annotations
from pydantic import BaseModel
from typing import ForwardRef, Optional, List
import httpx
from datetime import datetime

# model_backend = os.environ.get("BACKEND_API_HOST")
model_backend = "http://localhost:8000/client/"


class BackendAPIError(Exception):
    pass

CategoryRef = ForwardRef("Category")


class CreateMixin():
    def create(self):

        data = self.model_dump()

        user = self.__class__(data=data)

        res = httpx.post(f"{model_backend}{self.resource_path}", data=data)

        if res.status_code != 201:
            raise BackendAPIError(f"did not create resource, response with status code {res.status_code}")

        return user
    
class UpdateMixin():
    def update(self):
        pass

class DeleteMixin():
    def delete(self) -> True:
        id = self.model_dump().get("id")

        res = httpx.delete(f"{model_backend}{self.resource_path}{id}/")        


        if res.status_code != 204:
            raise BackendAPIError(f"did not create resource, response with status code {res.status_code}")
        
        return True

class ReadMixin():
    def read(self, pk : int | None, data : dict | None):
        if pk != None:

            if data != None:
                raise ValueError("data must not be provided if pk is optional")

            res = httpx.get(f"{model_backend}{self.resource_path}{pk}/")

            if res.status_code != 200:
                raise BackendAPIError(f"error getting resource, status code {res.status_code}")
                
            data = res.json()
        return data

class ListMixin():
    @classmethod
    def all(cls, *args, **kwargs):
        res = httpx.get(f"{model_backend}{cls.resource_path}", params=kwargs)

        if res.status_code != 200:
            raise BackendAPIError(f"error getting resource, status code {res.status_code}")
        
        data = res.json()

        return [cls(data=each) for each in data]
        


class Category(BaseModel, ReadMixin, ListMixin):
    id: int
    name: Optional[str] = None
    emoji: Optional[str] = None
    parent: Optional[int] = None
    children: Optional[List[int]] = None


    def __init__(self, pk : int | None = None, data : dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    @property
    def resource_path(self):
        return f"category/"




class User(BaseModel, CreateMixin, DeleteMixin, ReadMixin):
    id: int
    is_bot: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    date_created : Optional[datetime] = None

    def __init__(self, pk : int | None = None, data : dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    @property
    def resource_path(self):
        return f"user/"





class Product(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    id : int
    name: str
    price: Optional[float]
    category: Optional[int]
    sold: Optional[bool]


    def __init__(self, pk : int | None = None, data : dict | None = None):
        super().__init__(**self.read(pk, data))

    @classmethod
    @property
    def resource_path(self):
        return f"product/"

class Click(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    id : int
    type : Optional[str]
    name : Optional[str]
    user : Optional[int]

    def __init__(self, pk : int | None = None, data : dict | None = None):
        super().__init__(**self.read(pk, data))   

    @classmethod
    @property
    def resource_path(self):
        return f"click/"
    
class Notification(BaseModel, ReadMixin, CreateMixin, DeleteMixin, ListMixin):
    id : int
    user : Optional[int]
    category : Optional[int]

    def __init__(self, pk : int | None = None, data : dict | None = None):
        super().__init__(**self.read(pk, data))   

    @classmethod
    @property
    def resource_path(self):
        return f"notification/"
