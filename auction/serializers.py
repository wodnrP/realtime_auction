from rest_framework import serializers
from .models import Auction


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = "__all__"
        # read_only_fields = (
        #     "auction_user",
        #     "auction_product_name",
        #     "auction_start_at",
        #     "auction_participants",
        #     "auction_final_buyer",
        # )
