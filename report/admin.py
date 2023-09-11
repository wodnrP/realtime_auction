from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "reporter",
        "report_type",
        "report_at",
    )
    list_display_links = (
        "pk",
        "reporter",
        "report_type",
        "report_at",
    )
    list_filter = (
        "report_type",
        "report_at",
    )
    search_fields = ("reporter",)
