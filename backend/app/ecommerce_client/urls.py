from django.urls import path
from ecommerce_client import views

urlpatterns = [
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('product/', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path("user/", views.UserListView.as_view(), name="user-list"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("notification/", views.NotificationListView.as_view(), name="notification-list"),
    path("notification/<int:pk>/", views.NotificationListView.as_view(), name="notification-detail"),
    path("click/", views.ClickListView.as_view(), name= "click-list"),
    path("click/<int:pk>/", views.ClickDetailView.as_view(), name = "click-detail")
]
