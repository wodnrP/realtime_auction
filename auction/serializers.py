from rest_framework import serializers
from .models import AuctionRoom, AuctionMessage
from user.serializers import UserSerializer
from product.serializers import ProductsSerializer


class AuctionRoomSerializer(serializers.ModelSerializer):
    auction_host = serializers.StringRelatedField(read_only=True)
    auction_winner = serializers.StringRelatedField(read_only=True)
    auction_room_name = ProductsSerializer(read_only=True)
    paticipant_count = serializers.SerializerMethodField(read_only=True)
    auction_end_at = serializers.SerializerMethodField(read_only=True)

    def get_paticipant_count(self, obj):
        return obj.auction_paticipants.count()

    def get_auction_end_at(self, obj):
        formatted_time = obj.auction_end_at.strftime("%Y년 %m월 %d일 %H시 %M분 %S초") # 24시간제로 표시
        return formatted_time

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
            "auction_end_at",
        )

        read_only_fields = (
            "pk",
            "auction_host",
            "auction_winner",
            "auction_final_price",
            "auction_active",
            "auction_end_at",
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
