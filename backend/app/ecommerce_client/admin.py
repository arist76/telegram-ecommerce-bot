from django.contrib import admin
from ecommerce_client.models import Product, Click, Saved, Notification, User, Category
from django.contrib import admin
from .models import Category, Product, User, Notification, Saved, Click, ProductImage


# Register your models here.

admin.site.register(Product)
admin.site.register(Click)
admin.site.register(Saved)
admin.site.register(Notification)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(ProductImage)

# yourapp/resources.py


# class CategoryResource(resources.ModelResource):
#     class Meta:
#         model = Category
#         fields = ("id", "name", "emoji", "parent")


# class ProductResource(resources.ModelResource):
#     class Meta:
#         model = Product
#         fields = ("name", "price", "category", "sold")


# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User
#         fields = ("id", "is_bot", "first_name", "last_name", "username")


# class NotificationResource(resources.ModelResource):
#     class Meta:
#         model = Notification
#         fields = ("user", "category")


# class SavedResource(resources.ModelResource):
#     class Meta:
#         model = Saved
#         fields = ("user", "category")


# class ClickResource(resources.ModelResource):
#     class Meta:
#         model = Click
#         fields = ("user", "type", "name", "date")


# @admin.register(Category)
# class CategoryAdmin(ImportExportModelAdmin):
#     resource_class = CategoryResource


# @admin.register(Product)
# class ProductAdmin(ImportExportModelAdmin):
#     resource_class = ProductResource


# @admin.register(User)
# class UserAdmin(ImportExportModelAdmin):
#     resource_class = UserResource


# @admin.register(Notification)
# class NotificationAdmin(ImportExportModelAdmin):
#     resource_class = NotificationResource


# @admin.register(Saved)
# class SavedAdmin(ImportExportModelAdmin):
#     resource_class = SavedResource


# @admin.register(Click)
# class ClickAdmin(ImportExportModelAdmin):
#     resource_class = ClickResource
