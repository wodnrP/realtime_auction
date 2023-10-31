from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import Payments
from .serializers import (
    WinningBidListSerializer,
    KakaoPayReadySerializer,
    KakaoPayApprovalSerializer,
    KakaoCancelSerializer,
    KakaoFailSerializer,
)
from rest_framework.response import Response
import requests
from payment.tasks import create_payment_for_auction_winner  # Celery 작업 가져오기
from auction.models import AuctionRoom
from rest_framework import status
from payment.payment_platform.kakao_pay import KakaoPay
import json

# 프론트 세션,쿠키,캐시 대용
payment_dic={}

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
                try: 
                    if AuctionRoom.objects.get(pk=room_id, payment_active=False):
                        create_payment_for_auction_winner.delay(room_id)
                except:
                    print("Fail creating payment instance error")

            return Response(
                "Creating Payments in progress.", status=status.HTTP_202_ACCEPTED
            )
        else:
            # 낙찰 목록이 존재하면, JSON 형식으로 직렬화하여 반환
            total_bids = Payments.objects.filter(buyer=request.user, paid=False)
            serializer = WinningBidListSerializer(total_bids, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class KakaoPayReady(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        payment_id = request.data.get("paymentId")
        ##### TODO: Task1  프론트 생기면 해당 작업 수정 
        global payment_dic
        payment_dic[request.user] = payment_id
        ####

        payment = get_object_or_404(Payments, pk=payment_id)
        id = payment.pk
        user = payment.buyer
        product_name = payment.product_name
        total_amount = payment.total_price

        kakao_pay = KakaoPay()
        kakao_pay.kakao_pay_ready(
            id=id, user=user, product_name=product_name, total_amount=total_amount
        )
        # 터미널에서 카카오 페이 링크 소스 확인
        print(kakao_pay)

        ##### TODO: Task1. 프론트작업
        data = {"KaKaoURL": str(kakao_pay)}
        json_dumps_data = json.dumps(data)
        json_data = json.loads(json_dumps_data)

        serializer = KakaoPayReadySerializer(data=json_data)

        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=400)

        #####

    def get(self, request):
        # TODO: Task1. 프론트 생기면 해당 작업 수정 
        # global 딕셔너리 사용 -> 프론트 생기면 수정해야함
        global payment_dic
        
        if payment_dic[request.user]:
            try:
                obj = Payments.objects.get(pk=payment_dic[request.user], paid=False)
                serializer = KakaoPayReadySerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Payments.DoesNotExist:
                return Response(
                    {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class KakaoPayApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # TODO: Task1. 프론트 생기면 해당 작업 수정 
        # global 딕셔너리 사용 -> 프론트 생기면 수정해야함
        global payment_dic

        # 여기도 쿠키로 값을 만들어서 해야함
        payment = get_object_or_404(
            Payments, pk=payment_dic[request.user], paid=False, kakao_tid__isnull=False
        )
        id = payment.pk
        user = payment.buyer.phone_number
        tid = payment.kakao_tid

        kakao_pay = KakaoPay()
        kakao_pay.kakao_pay_approval(
            request=request,
            id=id,
            user=user,
            tid=tid,
        )

        data = {"di": "dsd"}
        return Response(data)

    def get(self, request):

        try:
            # TODO: Task1. 프론트 생기면 해당 작업 수정 
            # global 딕셔너리 사용 -> 프론트 생기면 수정해야함
            global payment_dic
            obj = Payments.objects.get(payment_dic[request.user], paid=True)
            serializer = KakaoPayApprovalSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payments.DoesNotExist:
            return Response(
                {"error": "Approved payment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class KakaoPayCancelView(APIView):
    def get(self, request):
        data = {"message": "Payment Cancel."}
        serializer = KakaoCancelSerializer(data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class KakaoPayFailView(APIView):
    def get(self, request):
        data = {"message": "Payment Fail."}
        serializer = KakaoFailSerializer(data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
