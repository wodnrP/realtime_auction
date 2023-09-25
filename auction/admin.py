from django.contrib import admin
from .models import Auction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "auction_users",
        "auction_chat_name",
        "auction_chat_open_at",
    )

    list_display_links = (
        "auction_users",
        "auction_chat_name",
    )

    list_filter = ("auction_chat_open_at",)

    search_fields = (
        "auction_users",
        "auction_chat_name",
        "auction_chat_open_at",
    )
