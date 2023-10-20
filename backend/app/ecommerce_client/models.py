# from django import utils
from django.db import models

from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from app import settings


class BaseMixin(models.Model):
    class Meta:
        abstract = True


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=25)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}{self.emoji}"

    @classmethod
    def get_grand_parent_id(cls, parent_id: int) -> int:
        parent = cls.objects.get(id=parent_id)
        return parent.parent


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    sold = models.BooleanField()

    @classmethod
    def paginate_by_category(cls, category_id: int, page_no: int = 1):
        category = Category.objects.get()
        products = cls.objects.filter(category=category_id)
        paginated_product = Paginator(products, settings.ITEMS_PER_PAGE)

        return paginated_product.page(page_no)

    def __str__(self) -> str:
        return f"{self.name}"


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name or ''}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)


class Click(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


# TODO - make the db query lazy
@sync_to_async
def async_filter(_Model: models.Model, **kwargs):
    return list(_Model.objects.filter(**kwargs))


@sync_to_async
def async_paginate(products, _id):
    paginated_products = Paginator(products, settings.ITEMS_PER_PAGE)

    return list(paginated_products.page(_id))
