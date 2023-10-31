from django.urls import path
from payment import views

urlpatterns = [
    path(
        "winning-bid-list", views.WinningdBidListView.as_view(), name="winning_bid_list"
    ),
    # Kakao
    path("kakao-pay-ready", views.KakaoPayReady.as_view(), name="kakao_pay"),
    path(
        "kakao-pay-approval",
        views.KakaoPayApprovalView.as_view(),
        name="kakao_pay_approval",
    ),
    path(
        "kakao-pay-cancel", views.KakaoPayCancelView.as_view(), name="kakao_pay_cancel"
    ),
    path("kakao-pay-fail", views.KakaoPayFailView.as_view(), name="kakao_pay_fail"),
]
