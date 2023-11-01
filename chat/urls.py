from django.urls import path

from .views import ChatRoomView

urlpatterns = [
    path("chat/<int:chat_pk>", ChatRoomView.as_view(), name="chat-room"),
]