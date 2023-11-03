from django.urls import path

from penalty import views

urlpatterns = [
    path("<int:user_id>", views.PenaltyView.as_view(), name="penalty"),
]
