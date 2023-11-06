from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from penalty.serializers import (PenaltySerializer, 
                                 BuyPenaltyReasonSerializer, SellPenaltyReasonSerializer)
from penalty.models import Penalty
from user.models import User


class PenaltyView(APIView):
    """
    get : 마이페이지에서 유저가 받은 페널티 내역 확인
    post : 유저에게 패널티 부여
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        penalty = Penalty.objects.get(user_id=user_id)
        serializer = PenaltySerializer(penalty, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyPenaltyReasonView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        user = User.objects.get(id=user_id)
        penalty,created = Penalty.objects.get_or_create(user_id=user)
        serializer = BuyPenaltyReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(penalty_id=penalty)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellPenaltyReasonView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        user = User.objects.get(id=user_id)
        penalty,created = Penalty.objects.get_or_create(user_id=user)
        serializer = SellPenaltyReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(penalty_id=penalty)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
