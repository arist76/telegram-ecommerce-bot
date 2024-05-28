from django.urls import path
from ecommerce_client import views

urlpatterns = [
    path("category/", views.CategoryList.as_view(), name="category-list"),
    path(
        "category/<uuid:uuid>/", views.CategoryDetail.as_view(), name="category-detail"
    ),
    path("product/", views.ProductListView.as_view(), name="product-list"),
    path(
        "product/<uuid:uuid>/", views.ProductDetailView.as_view(), name="product-detail"
    ),
    path(
        "product/<uuid:uuid>/image/",
        views.ProductImageListCreateView.as_view(),
        name="product-image",
    ),
    path("user/", views.UserListView.as_view(), name="user-list"),
    path("user/<uuid:id>/", views.UserDetailView.as_view(), name="user-detail"),
    path("user/<int:id>/", views.UserDetailView.as_view(), name="user-detail-by-id"),
    path(
        "notification/", views.NotificationListView.as_view(), name="notification-list"
    ),
    path(
        "notification/<uuid:uuid>/",
        views.NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path("click/", views.ClickListView.as_view(), name="click-list"),
    path("click/<uuid:uuid>/", views.ClickDetailView.as_view(), name="click-detail"),
    path("saved/", views.SavedListView.as_view(), name="saved-list"),
]
