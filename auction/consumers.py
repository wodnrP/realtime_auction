import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import AuctionRoom, AuctionMessage

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["auction_pk"]
        self.room_group_name = f"auction_{self.room_name}"
        self.user = self.scope["user"]

        # 로그인 된 사용자만 채팅에 참여 가능
        if not self.user.is_authenticated:
            await self.close()

        host = await self.get_auction_room()

        if not host:
            await self.close()
        else:
            self.host = host

        # 사용자를 채팅방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()
        await self.send_message(f"{self.user.nickname} 님이 입장하셨습니다.")
        await self.enter_or_exit_room("enter")

    async def disconnect(self, close_code):
        await self.send_message(f"{self.user.nickname}님이 퇴장하셨습니다.")
        await self.enter_or_exit_room("exit")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if not message_type or message_type not in ["send_message", "bid_price"]:
            return

        if message_type == "send_message":
            message = text_data_json["message"]
            await self.send_message(message)

        elif message_type == "bid_price":
            if self.host == self.user:
                await self.send(
                    text_data=json.dumps(
                        {"type": "error_message", "message": "host는 금액을 제시할 수 없습니다."}
                    )
                )
            else:
                bid_price = text_data_json["bid_price"]
                await self.create_or_update_auction_message(
                    self.user, self.room_name, bid_price
                )
                max_price_check = await self.update_max_price(bid_price)
                if max_price_check:
                    await self.send_bid_price(bid_price)
                    await self.send_message(f"현재 최고 금액 제시자는 {self.user.nickname}님 입니다.")

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
    def get_auction_room(self):
        room = AuctionRoom.objects.filter(pk=self.room_name)

        if not room.exists():
            return False

        elif not room[0].auction_active:
            return False

        return room[0].auction_host

    @database_sync_to_async
    def enter_or_exit_room(self, txt):
        """
        auction room 입장 시 auction_participants에 참가자 추가
        auction_end_at 전에 퇴장 시 auction_participants에서 참가자 제거
        > auction_participants에는 경매에 끝까지 참여한 사람이 남음
        """
        auction_room = AuctionRoom.objects.get(pk=self.room_name)

        if txt == "enter" and (self.user not in auction_room.auction_paticipants.all()):
            auction_room.auction_paticipants.add(self.user)

        elif txt == "exit" and auction_room.auction_end_at > timezone.now():
            auction_room.auction_paticipants.remove(self.user)

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
                    return True
                else:
                    if auction_message[0].auction_bid_price < bid_price:
                        auction_message.update(auction_bid_price=bid_price)
                        return True
                    return False

        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def update_max_price(self, bid_price):
        auction_room = AuctionRoom.objects.get(pk=self.room_name)
        auction_final_price = auction_room.auction_final_price
        if auction_final_price < bid_price:
            auction_room.auction_final_price = bid_price
            auction_room.auction_winner = self.user
            auction_room.save()
            return True
        return False
