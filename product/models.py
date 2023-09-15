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
    product_price = models.CharField(max_length=100)
    product_content = models.TextField()
    auction_start_at = models.DateTimeField()
    auction_end_at = models.DateTimeField()
    auction_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.id:
            # 모델이 생성될 때만 현재 시간을 설정
            self.auction_start_at = timezone.now()
            # 예시로 3일 후로 설정
            self.auction_end_at = timezone.now() + timezone.timedelta(days=3)
        super(Products, self).save(*args, **kwargs)

    @receiver(post_save, sender="product.Products")
    def set_auction_active(sender, instance, **kwargs):
        if not instance.auction_end_at or instance.auction_end_at < timezone.now():
            instance.auction_active = False
            instance.save()

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
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["category_name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class CategoryItem(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "CategoryItem"
        verbose_name_plural = "CategoryItems"

    def __str__(self):
        return f" category_id : {self.category_id}, product_id : {self.product_id}"
