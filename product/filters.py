from django_filters import rest_framework as filters
from .models import Products


class ProductsFilter(filters.FilterSet):
    class Meta:
        model = Products
        fields = {"category"}
