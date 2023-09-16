from rest_framework import serializers
from .models import Products, ProductImages


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("product_images",)


class ProductsSerializer(serializers.ModelSerializer):
    product_images = ImageSerializer(
        many=True, read_only=True, source="productimages_set"
    )

    class Meta:
        model = Products
        fields = "__all__"

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if data["product_images"]:
            data["product_images"] = data["product_images"][0]["product_images"]

        return data
