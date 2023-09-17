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

    category_name = serializers.CharField(
        source="category.category_name", required=True
    )

    class Meta:
        model = Products
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        image_urls = [img["product_images"] for img in data["product_images"]]
        data["product_images"] = image_urls

        data["category"] = data["category_name"]
        del data["category_name"]

        return data
