from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from ecommerce_client import models, serializers
from ecommerce_client.chroma_client import Chromaclient
from datetime import datetime
import sys

# chroma_client = Chromaclient()

class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
class CategoryDetail(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryWithChildrenSerializer
    lookup_field = "uuid"

class ProductListView(generics.ListCreateAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        # TODO: make proper validations for query parameters
        queryset = models.Product.objects.all()

        query = self.request.query_params.get('query')
        limit = int(self.request.query_params.get('limit', sys.maxsize))
        
        if query == None:
            offset = int(self.request.query_params.get('offset', 0))
            sort_by_price = self.request.query_params.get('sort-price')
            category = self.request.query_params.get('category')
            min_price = self.request.query_params.get('min-price')
            max_price = self.request.query_params.get('max-price')
            is_sold = self.request.query_params.get('is-sold')
            seller = self.request.query_params.get('seller')
            from_date = self.request.query_params.get('from')
            to_date = self.request.query_params.get('to')
    
            if sort_by_price == 'true':
                queryset = queryset.order_by('price')
            elif sort_by_price == 'false':
                queryset = queryset.order_by('-price')

            if category:
                queryset = queryset.filter(category__name=category)

            if min_price:
                queryset = queryset.filter(price__gte=float(min_price))

            if max_price:
                queryset = queryset.filter(price__lte=float(max_price))

            if is_sold == 'true':
                queryset = queryset.filter(sold=True)
            elif is_sold == 'false':
                queryset = queryset.filter(sold=False)

            if seller:
                queryset = queryset.filter(seller_id=seller)

            if from_date:
                from_date = datetime.fromisoformat(from_date)
                queryset = queryset.filter(posted__gte=from_date)

            if to_date:
                to_date = datetime.fromisoformat(to_date)
                queryset = queryset.filter(posted__lte=to_date)
        # else:
        #     return chroma_client.query(q=query, n_results=limit)
  
        return queryset[offset:offset+limit]
    
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
        return models.ProductImage.objects.filter(product_id=self.kwargs['uuid'])

    def perform_create(self, serializer):
        product_id = self.kwargs['uuid']
        product = models.Product.objects.get(uuid=product_id)
        serializer.save(product=product)


class UserListView(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "uuid"

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