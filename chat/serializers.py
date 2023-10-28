from rest_framework import serializers
from .models import Chatting, Message
from auction.serializers import AuctionRoomSerializer

class ChattingSerializer(serializers.ModelSerializer):
    auction_id = AuctionRoomSerializer(read_only=True)

    class Meta:
        model = Chatting
        fields = ("pk", "auction_id")

class MessageSerializer(serializers.ModelSerializer):
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
        model = Message
        fields = "__all__"