from django.urls import path

from user import views

urlpatterns = [
    path("sms/", views.CheckPhoneNumberVeiw.as_view(), name="send-sms"),
]
