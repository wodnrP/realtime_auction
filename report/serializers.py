from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    auction_id = serializers.StringRelatedField(read_only=True)
    report_chatting_room = serializers.StringRelatedField(read_only=True)
    reporter = serializers.StringRelatedField(read_only=True)
    report_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = (
            "pk",
            "auction_id",
            "report_chatting_room",
            "reporter",
            "report_type",
            "report_at",
        )
