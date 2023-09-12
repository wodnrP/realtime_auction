from djongo import models
from user.models import User
from product.models import Products
# Create your models here.


class Payments(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
