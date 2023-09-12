from django.urls import path

from user import views

urlpatterns = [
    path("sms/", views.CheckPhoneNumberView.as_view(), name="send-sms"),
    path("auth/", views.CheckAuthNumberView.as_view(), name="check-auth-number"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
