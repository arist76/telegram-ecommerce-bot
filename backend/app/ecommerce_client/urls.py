from django.urls import path
from ecommerce_client import views

urlpatterns = [
    path("user/<id:int>", views.category_by_parent, name="user"),
    path("category/<int:id>", views.test, name="category"),
    path(
        "category/<int:id>/children",
        views.category_grand_parent,
        name="subcategories",
    ),
    path("category/<int:id>/siblings", views.test, name="sibling_categories"),
    path("products/"),
    path("products/<int:id>"),
    path("products/<>"),
]
