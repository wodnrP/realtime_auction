from django.db import models

# Create your models here.


class Payments(models.Model):
    buyer = models.ForeignKey("user.users", on_delete=models.CASCADE)
    product_id = models.ForeignKey("product.products", on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
