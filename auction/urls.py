from django.urls import path
from django.conf import settings
from .views import AuctionListView, AuctionRoomView, AuctionMessageView


urlpatterns = [
    path("list/", AuctionListView.as_view(), name="auction-list"),
    path("room/", AuctionRoomView.as_view(), name="auction-room"),
    path("message/", AuctionMessageView.as_view(), name="auction-message"),
]