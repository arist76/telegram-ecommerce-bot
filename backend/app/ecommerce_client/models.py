# from django import utils
from django.db import models

from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from app import settings


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=25)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}{self.emoji}"


class Product(models.Model):
    id = models.BigIntegerField(primary_key=True)
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
    # seller

    @classmethod
    def paginate_by_category(cls, category_id: int, page_no: int = 1):
        category = Category.objects.get()
        products = cls.objects.filter(category=category_id)
        paginated_product = Paginator(products, settings.ITEMS_PER_PAGE)

        return paginated_product.page(page_no)

    def __str__(self) -> str:
        return f"{self.name}"


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name or ''}"


class Notification(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # seller

class Saved(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)


class Click(models.Model):
    id = models.BigIntegerField(primary_key=True)
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