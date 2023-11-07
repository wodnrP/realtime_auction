from django.urls import path
from django.conf import settings
from .views import ReportListView, ReportMessageView

urlpatterns = [
    path("list/", ReportListView.as_view(), name="report-list"),
    path(
        "message/<int:chatting_id>/", ReportMessageView.as_view(), name="report-message"
    ),
]
