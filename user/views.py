import random

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers import (
    UserSerializer,
    PhoneNumberSerializer,
    MyTokenObtainPairSerializer,
    LogoutSerializer,
)

from user.naver_sms.utils import make_signature, send_sms


class CheckPhoneNumberView(APIView):
    """
    Ncloud를 이용한 인증 번호 확인 API
    """

    def post(self, request):
        phone_serializer = PhoneNumberSerializer(data=request.data)
        signature, timestamp = make_signature()

        random_number = str(random.randrange(1000, 10000))
        phone_number = request.data["phone_number"]
        user_check = User.objects.filter(phone_number=phone_number).exists()

        if user_check:
            return Response(
                {"msg": "이미 존재하는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if phone_serializer.is_valid():
            res = send_sms(signature, timestamp, random_number, phone_number)

            if res.status_code >= 200 and res.status_code < 300:
                User.objects.create(
                    phone_number=phone_number, auth_number=random_number
                )
                return Response({"msg": "메세지 전송 완료"}, status=res.status_code)
            else:
                return Response({"msg": "메세지 전송 실패"}, status=res.status_code)
        return Response(
            {"error": phone_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class CheckAuthNumberView(APIView):
    """
    인증번호 일치 확인 API
    """

    def post(self, request):
        phone_number = request.data["phone_number"]
        input_number = request.data["input_number"]

        user_check = User.objects.filter(phone_number=phone_number)

        if user_check.exists():
            if user_check.first().auth_number == input_number:
                return Response({"msg": "인증이 완료되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({"msg": "저장된 번호가 없습니다."}, status=status.HTTP_404_NOT_FOUND)


class SignUpView(APIView):
    """
    인증번호 일치 확인 후 유저 추가 정보 설정 API
    """

    def put(self, request):
        phone_number = request.data["phone_number"]
        current_user = get_object_or_404(User, phone_number=phone_number)
        user_serializer = UserSerializer(current_user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"msg": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]

        user_check = User.objects.filter(phone_number=phone_number)

        if not user_check.exists():
            return Response(
                {"msg": "존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user_check.first().password):
            return Response(
                {"msg": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(phone_number=phone_number, password=password)

        if user.is_authenticated:
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {"msg": "로그인 성공", "access": access_token, "refresh": refresh_token},
                status=status.HTTP_200_OK,
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        """
        기존 유저 정보 조회
        """
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    
    def put(self, request):
        """
        개인 정보 수정 (닉네임, 주소, 비밀번호 등)
        """
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    """
    logout view
    """
    def post(self, request):
        token_serializer = LogoutSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        token_serializer.save()
        return Response({"msg": "logout success" }, 
                        status=status.HTTP_204_NO_CONTENT)
