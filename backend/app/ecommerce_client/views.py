from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from ecommerce_client import models, serializers, filters
from ecommerce_client.chroma_client import Chromaclient
from datetime import datetime
import sys
import uuid

# chroma_client = Chromaclient()


class AllPaginator(PageNumberPagination):
    page_size = 10000
    max_page_size = 10000


class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filterset_class = filters.CategoryFilter
    pagination_class = AllPaginator


class CategoryDetail(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryWithChildrenSerializer
    lookup_field = "uuid"


class ProductListView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_class = filters.ProductFilter


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    # TODO - fix if id in path and payload are different
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "uuid"


class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return models.ProductImage.objects.filter(product_id=self.kwargs["uuid"])

    def perform_create(self, serializer):
        product_id = self.kwargs["uuid"]
        product = models.Product.objects.get(uuid=product_id)
        serializer.save(product=product)


class UserListView(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self, queryset=None):
        # Get the 'pk' parameter from the URL
        pk = self.kwargs.get("id")

        # Check if 'pk' is a valid UUID
        try:
            uuid.UUID(str(pk))
            lookup_field = "uuid"
        except ValueError:
            lookup_field = "id"

        # Lookup the User object based on the determined field
        return get_object_or_404(models.User, **{lookup_field: pk})


class NotificationListView(generics.ListCreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    lookup_field = "uuid"


class ClickListView(generics.ListCreateAPIView):
    queryset = models.Click.objects.all()
    serializer_class = serializers.ClickSerializer


class ClickDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Click.objects.all()
    serializer_class = serializers.ClickSerializer
    lookup_field = "uuid"


class SavedListView(generics.ListCreateAPIView):
    queryset = models.Saved.objects.all()
    serializer_class = serializers.SavedSerializer
