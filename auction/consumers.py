# utils
import json
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# channels
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

# models
from .models import AuctionRoom, AuctionMessage
from product.models import Products
from user.models import User


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["auction_pk"]
        self.room_group_name = f"auction_{self.room_name}"
        self.user = self.scope["user"]

        # 로그인 된 사용자만 채팅에 참여 가능
        if not self.user.is_authenticated:
            await self.close()
            return

        # 사용자를 채팅방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # 입장 한 사람을 채팅방에 알림
        await self.send_message(f"{self.user.nickname} 님이 입장하셨습니다.")

        # 참여자 수 증가
        # await self.update_participant_count(1)

    async def disconnect(self, close_code):
        # user = self.scope["user"]
        # await self.send_message(f"{user.nickname}님이 퇴장하셨습니다.")
        await self.send_message(f"퇴장하셨습니다.")

        # 참여자 수 감소
        # await self.update_participant_count(-1)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if not message_type or message_type not in ["send_message", "bid_price"]:
            return

        if message_type == "send_message":
            message = text_data_json["message"]
            await self.send_message(message)

        elif message_type == "bid_price":
            bid_price = text_data_json["bid_price"]
            await self.send_bid_price(bid_price)
            await self.create_or_update_auction_message(
                self.user, self.room_name, bid_price
            )
            # await self.place_bid(bid_price)

    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "auction_message",
                "message": message,
            },
        )

    async def send_bid_price(self, bid_price):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "auction_bid_price",
                "bid_price": bid_price,
            },
        )

    async def auction_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "send_message",
                    "message": message,
                }
            )
        )

    async def auction_bid_price(self, event):
        bid_price = event["bid_price"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "bid_price",
                    "bid_price": bid_price,
                }
            )
        )

    @database_sync_to_async
    def create_or_update_auction_message(self, user, room_name, bid_price):
        try:
            auction_room = AuctionRoom.objects.filter(pk=room_name)
            if auction_room.exists():
                auction_message = AuctionMessage.objects.filter(
                    auction_room=auction_room[0], auction_user=user
                )
                if not auction_message.exists():
                    new_auction_message = AuctionMessage.objects.create(
                        auction_room=auction_room[0],
                        auction_user=user,
                        auction_bid_price=bid_price,
                    )
                    new_auction_message.save()
                else:
                    auction_message.update(auction_bid_price=bid_price)

        except ObjectDoesNotExist:
            return None

    # @database_sync_to_async
    # def update_participant_count(self, count_change):
    #     room = AuctionRoom.objects.get(auction_room=self.room_name)
    #     room.paticipant_count += count_change
    #     room.save()

    # async def check_auction_ended(self):
    #     room = await self.get_auction_room()
    #     if not room:
    #         return False

    #     expected_end_time = room.auction_start_at + timedelta(minutes=30)
    #     last_bid_time = expected_end_time + timedelta(seconds=30)

    #     if datetime.now(timezone.utc) >= last_bid_time:
    #         room.auction_end_at = datetime.now(timezone.utc)
    #         room.save()
    #         return True
    #     return False

    # @database_sync_to_async
    # def _update_bid(self, bid_price, user):
    #     room = AuctionRoom.objects.get(auction_room=self.room_name)
    #     last_bid_price = room.auction_final_price or room.starting_price

    #     if bid_price <= last_bid_price:
    #         return False

    #     room.auction_final_price = bid_price
    #     room.auction_winner = user
    #     room.save()
    #     return True

    # async def place_bid(self, bid_price):
    #     # 동시성 문제를 해결하기 위한 락
    #     async with transaction.atomic():
    #         # 경매가 종료되었는지 확인
    #         if await self.check_auction_ended():
    #             await self.send_message("경매가 종료되었습니다.")
    #             return False

    # updated = await database_sync_to_async(self._update_bid)(bid_price, self.scope["user"])

    # if updated:
    # 메시지로 입찰 정보를 전송하지만, 데이터베이스에는 저장하지 않음.
    # await self.send_message(f"{self.scope['user'].nickname}님이 {bid_price}원으로 입찰하셨습니다.")
