from django.urls import re_path
from .consumers import AuctionConsumer


websocket_urlpatterns = [
    # 경매 pk로 경매 채팅방 접속
    re_path(r"ws/auction/(?P<pk>\d+)/$", AuctionConsumer.as_asgi()),
]
