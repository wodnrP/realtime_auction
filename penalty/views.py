from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from penalty.serializers import PenaltySerializer
from penalty.models import Penalty

class PenaltyView(APIView):
    '''
    get : 마이페이지에서 유저가 받은 페널티 내역 확인
    post : 유저에게 패널티 부여
    '''
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        penalties = Penalty.objects.filter(user_id=user_id)
        serializer = PenaltySerializer(penalties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, user_id):
        serializer = PenaltySerializer(data = request.data)
        if serializer.is_vaid():
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)