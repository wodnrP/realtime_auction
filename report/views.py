from django.shortcuts import render
from .serializers import ReportSerializer

from .models import Report
from chat.models import Message
from penalty.models import Penalty

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied


class ReportListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class CreateReportView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근할 수 있도록

    def post(self, request):
        message_id = request.data.get("message_id")
        report_type = request.data.get("report_type")

        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response(
                {"message": "메세지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        if message.sender_id == request.user:
            return Response(
                {"message": "자신의 메세지는 신고할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        report = Report.objects.create(
            reporter=request.user,
            report_criminal=message.sender_id,
            report_chatting_room=message.chatting_id,
            report_type=report_type,
            report_content=message.message_content,
        )

        penalty_type = "sell" if request.user.is_seller else "buy"

        penalty, created = Penalty.objects.get_or_create(
            user_id=message.sender_id,
            defaults={
                "penalty_type": penalty_type,
                "penalty_content": report_type,
            },
        )
        
        if not created:
            penalty.penalty_points += 1
            penalty.save()

        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
