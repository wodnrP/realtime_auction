from django_filters import rest_framework as filters
from .models import Products


class ProductsFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name="product_name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__category_name", lookup_expr="icontains")

    class Meta:
        model = Products
        fields = ("category", "keyword")
