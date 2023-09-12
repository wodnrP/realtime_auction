from djongo import models
from user.models import User
from product.models import Products
# Create your models here.
class Wishlist(models.Model):
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    wishlist_active = models.BooleanField(default=False)

