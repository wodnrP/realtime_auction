from django.contrib import admin
from .models import Wishlist
# Register your models here.

class WishlistAdmin(admin.ModelAdmin):
    list_display = [
        'users_id',
        'product_id'
    ]

admin.site.register(Wishlist, WishlistAdmin)
