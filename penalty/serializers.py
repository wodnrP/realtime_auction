from rest_framework import serializers
from penalty.models import Penalty,BuyPenaltyReason,SellPenaltyReason


class PenaltySerializer(serializers.ModelSerializer):

    class Meta:
        model = Penalty
        fields = "__all__"
        read_only_fields = [
            "user_id",
        ]

class BuyPenaltyReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyPenaltyReason
        fields = "__all__"
        read_only_fields = [
            "penalty_id",
        ]

class SellPenaltyReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellPenaltyReason
        fields = "__all__"
        read_only_fields = [
            "penalty_id",
        ]