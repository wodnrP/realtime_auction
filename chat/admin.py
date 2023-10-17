from django.contrib import admin
from .models import Chatting, Message
# Register your models here.

@admin.register(Chatting)
class ChattingAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "auction_id",
    )

    list_display_links = (
        "pk",
        "auction_id",
    )

    search_fields = (
        "auction_id"
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "chatting_id",
        "sender_id",
        "message_type",
        "message_content",
        "message_time",
    )

    list_display_links = (
        "pk",
        "chatting_id",
        "sender_id",
        "message_type",
        "message_content",
        "message_time",
    )