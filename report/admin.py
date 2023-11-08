from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Report
from chat.models import Message


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "report_chatting_room",  # 신고 된 채팅방
        "reporter",  # 신고한 사람
        "report_criminal",  # 신고 당한 사람
        "report_type",
        "report_at",
    )
    list_display_links = (
        "pk",
        "report_chatting_room",
        "reporter",
        "report_criminal",
        "report_type",
        "report_at",
    )
    list_filter = (
        "report_type",
        "report_at",
    )
    search_fields = ("reporter",)
    
    def __str__(self):
        return self.report_chatting_room

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("report_chatting_room")
        return queryset
