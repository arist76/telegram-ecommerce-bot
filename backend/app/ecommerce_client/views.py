from django.shortcuts import render
from rest_framework.decorators import api_view
from ecommerce_client import models


@api_view(["GET"])
def category_by_parent(request, parent_id: str = 0):
    if parent_id == 0:
        return models.Category.objects.filter(parent__isnull=True)
    else:
        return models.Category.objects.filter(parent=parent_id)


def category_grand_parent(request):
    pass


def test(request):
    pass
