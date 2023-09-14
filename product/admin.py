from django.contrib import admin
from .models import Products, ProductImages, Categories, CategoryItem


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "seller_id",
        "product_price",
        "auction_start_at",
        "auction_end_at",
        "auction_state",
    )
    list_filter = ("seller_id", "auction_state")
    search_fields = ("product_name", "seller_id__username")


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("products_id", "product_images")


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("category_name",)


class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ("category_id", "product_id")


admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(CategoryItem, CategoryItemAdmin)
