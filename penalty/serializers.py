from rest_framework import serializers
from penalty.models import Penalty

class PenaltySerializer(serializers.ModelSerializer):
    buy_penalties_count = serializers.SerializerMethodField(read_only=True)
    sell_penalties_count = serializers.SerializerMethodField(read_only=True)
    
    def get_buy_penalties_count(self, obj):
        return Penalty.objects.filter(user_id = obj.user_id, penalty_type='buy').count()
    
    def get_sell_penalties_count(self, obj):
        return Penalty.objects.filter(user_id = obj.user_id, penalty_type='sell').count()
    
    class Meta:
        model = Penalty
        fields = '__all__'
        read_only_fields = ["user_id",]
        