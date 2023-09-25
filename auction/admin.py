from django.contrib import admin
from .models import AuctionRoom, AuctionMessage


@admin.register(AuctionRoom)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "auction_host",
        "auction_room_name",
        "auction_start_at",
    )

    list_display_links = (
        "pk",
        "auction_host",
        "auction_room_name",
    )

    search_fields = (
        "auction_host",
        "auction_room_name",
        "auction_start_at",
    )
