from django.urls import path

from .views import AuctionListView, UserAuctionListView, NewAuctionRoomView

urlpatterns = [
    path("list", AuctionListView.as_view(), name="auction-list"),
    path("list/<int:user_pk>", UserAuctionListView.as_view(), name="user-auction-list"),
    path("room/<int:room_pk>", NewAuctionRoomView.as_view(), name="auction-room"),
]