from django.shortcuts import render
from .serializers import AuctionRoomSerializer

from .models import AuctionRoom

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.db.models import Q
from django.shortcuts import get_object_or_404

 
class AuctionListView(APIView):
    def get(self, request):
        rooms = AuctionRoom.objects.all()
        serializer = AuctionRoomSerializer(rooms, many=True)
        return Response(serializer.data)


class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    # 경매 주최자 or 경매 낙찰자가 해당 유저인 경매 목록
    def get(self, request, user_pk):
        auction_rooms = AuctionRoom.objects.filter(Q(auction_host=user_pk) | Q(auction_winner=user_pk))
        serializer = AuctionRoomSerializer(auction_rooms, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)


class NewAuctionRoomView(APIView):
    permission_classes = [IsAuthenticated]
    #경매 입장시 마감시간, 최고 제시 가격 조회 역할
    def get(self, request, room_pk):
        room = get_object_or_404(AuctionRoom, pk=room_pk)
        serializer = AuctionRoomSerializer(room)
        return Response(serializer.data)

    def delete(self, request, room_pk):
        room = get_object_or_404(AuctionRoom, pk=room_pk)
        if room.auction_host != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
