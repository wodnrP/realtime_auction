from djongo import models

# Create your models here.
class WishList(models.Model):
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist_active = models.BooleanField(default=False)

