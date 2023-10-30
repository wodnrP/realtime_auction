from django.db import models
from user.models import User
from product.models import Products
from auction.models import AuctionRoom

# Create your models here.


class Payments(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    total_price = models.ForeignKey(AuctionRoom, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"구매자 : {self.buyer}, 낙찰아이템 : {self.product_name}"