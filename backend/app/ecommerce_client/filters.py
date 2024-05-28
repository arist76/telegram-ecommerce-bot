import django_filters
from ecommerce_client import models


class CategoryFilter(django_filters.FilterSet):
    parent_isnull = django_filters.BooleanFilter(
        field_name="parent", lookup_expr="isnull"
    )

    class Meta:
        model = models.Category
        fields = {
            "name": [
                "exact",
                "icontains",
            ],  # Allows filtering by exact match or case-insensitive contains
            "emoji": ["exact", "icontains"],
            "parent": ["exact"],  # Allows filtering by exact match on parent
            "uuid": ["exact"],  # Allows filtering by exact match on UUID
        }


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.UUIDFilter(field_name="category__uuid")
    posted_on_after = django_filters.DateTimeFilter(
        field_name="posted_on", lookup_expr="gte"
    )
    posted_on_before = django_filters.DateTimeFilter(
        field_name="posted_on", lookup_expr="lte"
    )
    last_modified_after = django_filters.DateTimeFilter(
        field_name="last_modified", lookup_expr="gte"
    )
    last_modified_before = django_filters.DateTimeFilter(
        field_name="last_modified", lookup_expr="lte"
    )
    sold = django_filters.BooleanFilter(field_name="sold")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    seller_chat = django_filters.CharFilter(
        field_name="seller_chat", lookup_expr="icontains"
    )
    q = django_filters.CharFilter(method="filter_by_query")
    saved_by = django_filters.CharFilter(method="filter_by_saved_user")

    class Meta:
        model = models.Product
        fields = [
            "price",
            "category",
            "sold",
            "name",
            "posted_on",
            "last_modified",
            "seller_chat",
        ]

    def filter_by_query(self, queryset, name, value):
        return queryset.order_by("?")[:1]

    def filter_by_saved_user(self, queryset, name, value):
        try:
            user = models.User.objects.get(id=value)
        except:
            return models.Product.objects.none()

        return queryset.filter(saved_product__user=user)
