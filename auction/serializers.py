from rest_framework import serializers
from .models import Auction, AuctionMessage
from user.serializers import UserSerializer


class AuctionMessageSerializer(serializers.ModelSerializer):
    last_bid_price = serializers.SerializerMethodField()

    class Meta:
        model = AuctionMessage
        depth = 1
        fields = "__all__"
        read_only_fields = "sendet_id", "auction_room"
    
    def get_last_bid_price(self, obj: AuctionMessage):
        return obj.auction_room.auction_final_price


class AuctionSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    messages = AuctionMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        depth = 1
        fields = "__all__"
        read_only_fields = "__all__"
        extra_kwargs = {
            "auction_final_buyer": {"required": False},
            "auction_final_price": {"required": False},
        }

    def get_created_at_formatted(self, obj: AuctionMessage):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
