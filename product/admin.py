from django.contrib import admin
from django import forms
from .models import Products, ProductImages, Categories
import admin_thumbnails


@admin_thumbnails.thumbnail("product_images")
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class ProductsAdminForm(forms.ModelForm):
    class Meta:
        model = Products
        fields="__all__"


class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = (
        "product_name",
        "seller_id",
        "product_price",
        "auction_start_at",
        "product_active",
        "auction_end_at"
    )
    list_filter = ("seller_id", "product_active")
    search_fields = ("product_name", "seller_id__username")
    inlines = [ProductImagesInline]


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("category_name",)


admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories, CategoriesAdmin)
