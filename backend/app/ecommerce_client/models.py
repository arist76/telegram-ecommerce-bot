# from django import utils
from django.db import models
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from app import settings
import uuid as uuid_gen
import os
import secrets


# category manager
class CategoryManager(models.Manager):
    def get_only_product_queryset(self) -> models.QuerySet:
        return Category.objects.annotate(products_count=models.Count("product")).filter(
            products_count__gt=0
        )


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    schema_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    objects = CategoryManager()

    def __str__(self) -> str:
        return f"Category: {self.name}"


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    sold = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    detailed_description = models.JSONField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    seller_chat = models.CharField(
        max_length=100, null=True, blank=True
    )  # TODO: this might need normalization
    seller_details = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Product: {self.name}"

    # NOTICE : if you override save() it will cause problems in signals
    # def save(self)


def product_image_upload_to(instance, filename):
    # Extract the seller's username or any unique identifier
    seller_id = (
        instance.product.seller_chat if instance.product.seller_chat else "default"
    )
    product_id = instance.product.uuid
    _, extension = os.path.splitext(filename)
    new_filename = str(instance.count) + extension

    # Create the upload path
    return os.path.join(f"sellers/{seller_id}/products/{product_id}", new_filename)


class ProductImage(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    count = models.IntegerField(unique=True, editable=False)
    image = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    def save(self, *args, **kwargs):
        if not self.count:
            product_count = ProductImage.objects.count()
            print(product_count)
            self.count = product_count + 1
        super().save(*args, **kwargs)


class Attribute(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    schema_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    friendly_id = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)

    def __str__(self):
        return f"Attribute: {self.name}"


class CategoryAttribute(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"Category to Attribute: {self.category.name} - {self.attribute.name}"


class ValueOption(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    schema_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    schema_friendly_id = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)

    def __str__(self):
        return f"Value Option: {self.name}"


class AttributeValueOptions(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(ValueOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attribute to Value: {self.attribute.name} - {self.value.name}"


class ProductAttribute(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_attributes"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # check if the attribute exists in the category
        if not self.attribute.category == self.product.category:
            raise ValueError("Attribute does not belong to the category")

        super().save(*args, **kwargs)


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    id = models.IntegerField(unique=True)  # The telegram ID
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name or ''}"


class Notification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # seller


class Saved(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE, related_name="saved_product")
    date = models.DateTimeField(auto_now_add=True)


class Click(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_gen.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
