# from django import utils
from django.db import models
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from app import settings
import uuid
import os
import secrets


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.BigIntegerField(unique=True)  # Must exist for hierachical reasons
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=25)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}{self.emoji}"

class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    sold = models.BooleanField()
    description = models.TextField(null=True)
    detailed_description = models.JSONField(null=True)
    posted = models.DateTimeField(null=True)
    last_modified = models.DateTimeField(null=True)
    seller_chat = models.CharField(max_length=100, null=True)  # TODO: this might need normalization 
    seller_details = models.TextField(null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    # NOTICE : if you override save() it will cause problems in signals
    # def save(self)


def product_image_upload_to(instance, filename):
    # Extract the seller's username or any unique identifier
    seller_id = instance.product.seller_chat if instance.seller_chat else 'default'
    _ , extension = os.path.splitext(filename)
    new_filename =  uuid.uuid() + extension

    # Create the upload path
    return os.path.join(f'sellers/{seller_id}/products/', new_filename)

class ProductImage(models.Model):
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name or ''}"


class Notification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # seller

class Saved(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)


class Click(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


"""
    User

    UserID (Primary Key)
    Username
    Password
    Email
    First Name
    Last Name
    Address
    Phone Number
    
    Product

    ProductID (Primary Key)
    Product Name
    Description
    Price
    Quantity
    CategoryID (Foreign Key)
    SellerID (Foreign Key)
    Date Posted
    
    Category

    CategoryID (Primary Key)
    Category Name
    
    Cart

    CartID (Primary Key)
    UserID (Foreign Key)
    Total Price
    
    CartItem

    CartItemID (Primary Key)
    CartID (Foreign Key)
    ProductID (Foreign Key)
    Quantity
    Subtotal Price
    
    Order

    OrderID (Primary Key)
    UserID (Foreign Key)
    Order Date
    Shipping Address
    Total Price
    
    OrderItem

    OrderItemID (Primary Key)
    OrderID (Foreign Key)
    ProductID (Foreign Key)
    Quantity
    Subtotal Price
    
    Review

    ReviewID (Primary Key)
    ProductID (Foreign Key)
    UserID (Foreign Key)
    Rating
    Comment
    Date Posted
    
    PaymentMethod

    PaymentMethodID (Primary Key)
    UserID (Foreign Key)
    Payment Type (e.g., Credit Card, PayPal, etc.)
    Card Number
    Expiration Date
    Address

    AddressID (Primary Key)
    UserID (Foreign Key)
    Street Address
    City
    State/Province
    Zip/Postal Code
    Country
"""