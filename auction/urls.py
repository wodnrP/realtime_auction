from django.urls import path
from django.conf import settings
from .views import AuctionListView, UserAuctionListView, AuctionRoomView, AuctionMessageView, index, room


urlpatterns = [
    path("", index, name="index"),
    path("<str:room_name>", room, name="room"),
    path("list", AuctionListView.as_view(), name="auction-list"),
    path("list/<int:user_pk>", UserAuctionListView.as_view(), name="user-auction-list"),
    path("room", AuctionRoomView.as_view(), name="auction-room"),
    path("message", AuctionMessageView.as_view(), name="auction-message"),
]