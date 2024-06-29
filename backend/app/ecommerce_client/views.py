from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ecommerce_client import models, serializers, filters
from ecommerce_client.chroma_client import Chromaclient
from datetime import datetime
import sys
import uuid


# chroma_client = Chromaclient()


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    filterset_class = filters.CategoryFilter

    def get_queryset(self):
        # annotate the sum of products under each category
        with_products = self.request.GET.get("with_products", False)

        if with_products:
            return models.Category.objects.get_only_product_queryset()

        return models.Category.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "with_products",
                openapi.IN_QUERY,
                description="Filter categories with product",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetail(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryWithChildrenSerializer
    lookup_field = "uuid"

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        serializer_class.context["with_products"] = self.request.GET.get(
            "with_products", False
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "with_products",
                openapi.IN_QUERY,
                description="Filter categories with product",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductListView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_class = filters.ProductFilter


class AttributeListView(generics.ListAPIView):
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer
    filterset_class = filters.AttributeFilter


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
