from django.urls import path
from django.conf import settings
from .views import ReportListView

urlpatterns = [
    path("list/", ReportListView.as_view(), name="report-list"),
]
