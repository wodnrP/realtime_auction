from django.db import models
from django.utils import timezone
# Create your models here.


class Products(models.Model):
    buyer_id = models.OneToOneField("auctions", on_delete=models.CASCADE, null=True, blank=True)
    seller_id = models.OneToOneField("users", on_delete=models.CASCADE)
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


class Product_images(models.Model):
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_images = models.ImageField()



    
