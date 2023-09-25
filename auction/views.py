from django.shortcuts import render
from .serializers import (
    AuctionRoomSerializer,
    AuctionRoomListSerializer,
    AuctionMessageSerializer,
)
from .models import AuctionRoom, AuctionMessage
from product.models import Products
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q, F


class AuctionListView(APIView):
    def get(self, request):
        rooms = AuctionRoom.objects.all()
        serializer = AuctionRoomListSerializer(rooms, many=True)
        return Response(serializer.data)


class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_pk = request.user.pk
        queryset = (
            Products.objects.filter(status=False, auction_winner__isnull=False)
            .filter(Q(auction_host=user_pk) | Q(auction_winner=user_pk))
            .annotate(updated_at=F("auction_room__updated_at"))
            .order_by("-updated_at")
            .select_related(
                "auction_room",
                "auction_room__auction_host",
                "auction_room__auction_winner",
                "auction_room__auction_final_price",
            )
            .prefetch_related("auction_room__auction_paticipants")
        )
        serializer = AuctionRoomListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class AuctionRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return AuctionRoom.objects.get(pk=pk)
        except AuctionRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = AuctionRoomSerializer(room)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuctionRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.auction_host != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuctionMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return AuctionRoom.objects.get(pk=pk)
        except AuctionRoom.DoesNotExist:
            raise NotFound

    def post(self, request):
        room_id = request.data.get("auction_room")
        bid_price = request.data.get("auction_bid_price")

        if not room_id or not bid_price:
            return Response(
                {"detail": "유효하지 않은 데이터 입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        room = AuctionRoom.objects.get(id=room_id)

        starting_price = room.starting_price
        last_bid_price = room.auction_final_price or starting_price

        if bid_price <= last_bid_price:
            return Response(
                {"detail": "입력 가격은 이전 가격보다 높아야합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AuctionMessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            room.auction_final_price = bid_price
            room.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
