from rest_framework import serializers
from .models import Products, ProductImages, Categories


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("product_images",)


class ProductsSerializer(serializers.ModelSerializer):
    product_images = ImageSerializer(
        many=True, read_only=True, source="productimages_set"
    )

    category_name = serializers.CharField(source="category.category_name")

    class Meta:
        model = Products
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # 'category' 필드 대신 'category_name' 필드 사용
        data["category"] = data["category_name"]
        del data["category_name"]

        if data["product_images"]:
            data["product_images"] = data["product_images"][0]["product_images"]

        return data
