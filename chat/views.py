from django.shortcuts import render
from . serializers import ChattingSerializer, MessageSerializer

from .models import Chatting, Message

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

# Create your views here.
class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, chat_pk):
        chat = get_object_or_404(Chatting, pk=chat_pk)
        serializer = ChattingSerializer(chat)
        return Response(serializer.data)

    # 경매 낙찰자와 판매자일 경우에만 삭제 가능
    def delete(self, request, chat_pk):
        chat = get_object_or_404(Chatting, pk=chat_pk)
        host = chat.auction_id.auction_host
        if chat.auction_id.auction_winner != request.user and host != request.user:
            raise PermissionDenied
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)