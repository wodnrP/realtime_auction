from django.contrib import admin
from penalty.models import Penalty


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "penalty_type",
        "penalty_content",
        "penalty_date",
    ]
