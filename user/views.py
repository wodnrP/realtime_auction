import random

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.serializers import UserSerializer, PhoneNumberSerializer

from user.naver_sms.utils import make_signature, send_sms

class CheckPhoneNumberVeiw(APIView):
    '''
    Ncloud를 이용한 인증 번호 확인 API
    '''
    def post(self, request):
        phone_serializer = PhoneNumberSerializer(data=request.data)
        signature, timestamp= make_signature()
        
        random_number = random.randrange(1000,10000)
        if phone_serializer.is_valid():
            phone_number = request.data['phone_number']
            res = send_sms(signature,timestamp, random_number, phone_number)

            if res.status_code >=200 and res.status_code < 300:
                return Response({"msg":"메세지 전송 완료"}, status=res.status_code)
            else:
                return Response({"msg":"메세지 전송 실패"}, status=res.status_code)
        return Response({"error":phone_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
