from django.urls import path

from penalty import views

urlpatterns = [
    path("<int:user_id>", views.PenaltyView.as_view(), name="penalty"),
    path("<int:user_id>/buy", views.BuyPenaltyReasonView.as_view(), name="buy_penalty"),
    path(
        "<int:user_id>/sell", views.SellPenaltyReasonView.as_view(), name="sell_penalty"
    ),
]
