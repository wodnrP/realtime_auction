from django.shortcuts import render
from .serializers import ReportSerializer

from .models import Report
from chat.models import Message

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class ReportListView(APIView):
    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class ReportMessageView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, chatting_id):
        try:
            message = Message.objects.get(chatting_id=chatting_id)
        except Message.DoesNotExist:
            return Response(
                {"message": "메세지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReportSerializer(message)
        return Response(serializer.data)

    def post(self, request, chatting_id):
        try:
            message = Message.objects.get(chatting_id=chatting_id)
        except Message.DoesNotExist:
            return Response(
                {"message": "메세지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReportSerializer(data=request.data)
        if serializer.is_vaild():
            report_type = serializer.validated_data.get("report_type")
            report_content = message.message_content
            reporter = request.user
            report_chatting_room = message.chatting_id
            report_at = message.message_at

            report = Report.object.create(
                reporter=reporter,
                report_chatting_room=report_chatting_room,
                report_type=report_type,
                report_at=report_at,
                report_content=report_content,
            )
            serializer.save(report.data)

            return Response(
                {"message": "메세지 신고가 접수되었습니다."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
