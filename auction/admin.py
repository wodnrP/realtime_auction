from django.contrib import admin
from .models import Auction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "auction_user",
        "auction_product_name",
        "auction_start_at",
    )

    list_display_links = (
        "pk",
        "auction_user",
        "auction_product_name",
    )

    list_filter = ("auction_start_at",)

    search_fields = (
        "auction_user",
        "auction_product_name",
        "auction_start_at",
    )
