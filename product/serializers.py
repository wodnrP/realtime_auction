from rest_framework import serializers
from .models import Products, ProductImages


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
