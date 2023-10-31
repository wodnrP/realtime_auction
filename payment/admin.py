from django.contrib import admin
from .models import Payments

# Register your models here.


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = [
        "buyer",
        "product_name",
        "payment_type",
        "payment_date",
        "get_auction_final_price",
        "paid",
    ]

    def get_auction_final_price(self, obj):
        return obj.total_price.auction_final_price if obj.total_price else None

    get_auction_final_price.short_description = "Auction Final Price"
