from django.db import models
from django.utils import timezone
from user.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Products(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_content = models.TextField()
    auction_start_at = models.DateTimeField(blank=False, null=False,default=timezone.now())
    # auction_end_at = models.DateTimeField(blank=True, null=True)
    auction_active = models.BooleanField(default=True)
    category = TreeForeignKey("Categories", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # @receiver(post_save, sender="product.Products")
    # def set_auction_active(sender, instance, created, **kwargs):
    #     if created:
    #         if not instance.auction_end_at or instance.auction_end_at < timezone.now():
    #             instance.auction_active = False
    #             instance.save(update_fields=["auction_active"])

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_images = models.ImageField(upload_to="product/images/")

    class Meta:
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        return self.products_id.product_name


class Categories(MPTTModel):
    category_name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["category_name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
