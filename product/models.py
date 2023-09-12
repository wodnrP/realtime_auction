from djongo import models
from django.utils import timezone
from user.models import User
# Create your models here.


class Products(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.CharField(max_length=100)
    product_content = models.CharField(max_length=100)
    auction_start_at = models.DateTimeField()
    auction_end_at = models.DateTimeField()
    auction_state = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.id:
            # 모델이 생성될 때만 현재 시간을 설정
            self.auction_start_at = timezone.now()
            # 예시로 3일 후로 설정
            self.auction_end_at = timezone.now() + timezone.timedelta(days=3)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_images = models.ImageField()


class Categories(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class CategoryItem(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f" category_id : {self.category_id}, product_id : {self.product_id}"
