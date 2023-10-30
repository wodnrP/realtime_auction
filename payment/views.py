from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import Payments
from .serializers import WinningBidListSerializer
from rest_framework.response import Response

from payment.tasks import create_payment_for_auction_winner  # Celery 작업 가져오기
from auction.models import AuctionRoom
from rest_framework import status


class WinningdBidListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 낙찰 목록 중 아직 지불되지 않은 낙찰 목록 필터링
        winning_bids = Payments.objects.filter(buyer=request.user)
        winning_auction = AuctionRoom.objects.filter(auction_winner=request.user)
        
        if len(winning_bids) != len(winning_auction):
            # 낙찰 목록이 없으면, 선택한 경매 방 (`AuctionRoom`)의 ID를 가져와서 Payment를 생성하는 샐러리 작업 실행
            room_ids = AuctionRoom.objects.filter(
                auction_winner=request.user
            ).values_list("pk", flat=True)
            

            for room_id in room_ids:
                room = AuctionRoom.objects.get(pk=room_id)
                
                create_payment_for_auction_winner.delay(room_id)
                
            return Response(
                "Creating Payments in progress.", status=status.HTTP_202_ACCEPTED
            )
        else:
            # 낙찰 목록이 존재하면, JSON 형식으로 직렬화하여 반환
            total_bids = Payments.objects.filter(buyer=request.user, paid=False)
            serializer = WinningBidListSerializer(total_bids, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class KakaoPayView(APIView):
    pass



class KakaoPayApprovalView(APIView):
    pass


class KakaoPayCancelView(APIView):
    pass