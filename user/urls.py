from django.urls import path

from user import views

urlpatterns = [
    path("sms", views.CheckPhoneNumberView.as_view(), name="send_sms"),
    path("auth", views.CheckAuthNumberView.as_view(), name="check_auth_number"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("my-page", views.ProfileView.as_view(), name="my_profile"),
]
