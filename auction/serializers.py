from rest_framework import serializers
from .models import AuctionRoom, AuctionMessage
from user.serializers import UserSerializer
from product.serializers import ProductsSerializer

class AuctionRoomSerializer(serializers.ModelSerializer):
    auction_room_name = ProductsSerializer(read_only=True)
    paticipant_count = serializers.SerializerMethodField(read_only=True)
    
    def get_paticipant_count(self, obj):
        return obj.auction_paticipants.count()
    
    class Meta:
        model = AuctionRoom
        fields = (
            "pk",
            "auction_host",
            "auction_room_name",
            "auction_winner",
            "auction_final_price",
            "paticipant_count",
            "auction_active",
            "auction_end_at"
        )

        read_only_fields = (
            "pk",
            "auction_host",
            "auction_winner",
            "auction_final_price",
            "auction_active",
            "auction_end_at"
        )


class AuctionMessageSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        time = obj.created_at
        am_pm = time.strftime("%p")
        now_time = time.strftime("%I:%M")

        if am_pm == "AM":
            now_time = f"오전 {now_time}"
        else:
            now_time = f"오후 {now_time}"
        return now_time

    class Meta:
        model = AuctionMessage
        fields = "__all__"
