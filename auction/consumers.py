import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import AuctionRoom, AuctionMessage


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 로그인 확인
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        # 경매방 이름
        self.auction_pk = self.scope["url_route"]["kwargs"]["auction_pk"]
        self.room_group_name = f"auction_{self.auction_pk}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        await self.add_participant()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        await self.remove_participant()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]

        room = await self.get_room(self.auction_pk)

        if not room or room.auction_active == False:
            await self.close()
            return

        # 메세지 유형 별 함수 호출
        function_mapping = {
            "join": self.handle_join,
            "bid": self.handle_bid,
            "message": self.handle_message,
        }

        if message_type in function_mapping:
            await function_mapping[message_type](text_data_json)

    async def handle_join(self, data):
        current_user = self.scope["user"]
        await self.add_participant()
        await self.send_welcome_message(current_user.username)

    async def handle_bid(self, data):
        current_user = self.scope["user"]
        room = await self.get_auction_room(self.auction_pk)

        if room.auction_host == current_user:
            await self.send_error_message("경매 주최자는 입찰할 수 없습니다.")
            return

        if room.auction_end_at < timezone.now():
            await self.send_error_message("경매가 종료되었습니다.")
            return

        new_bid = int(data["bid"])
        if new_bid > room.auction_bid_price:
            await self.update_bid_price(new_bid)
            await self.send_bid_message(current_user.username, new_bid)
        else:
            await self.send_error_message("현재 입찰가보다 높은 가격을 제시해주세요.")

    async def handle_message(self, data):
        current_user = self.scope["user"]
        room = await self.get_auction_room(self.auction_pk)

        if room.auction_host != current_user:
            await self.send_error_message("메세지는 경매 주최자만 보낼 수 있습니다.")
            return

        message = data["message"]
        await self.send_message_message(current_user.username, message)

    async def send_welcome_message(self, username):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_type": "join",
                "username": username,
            },
        )

    async def send_bid_message(self, username, bid):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_type": "bid",
                "username": username,
                "bid": bid,
            },
        )

    async def send_message_message(self, username, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_type": "message",
                "username": username,
                "message": message,
            },
        )

    async def send_error_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_type": "error",
                "message": message,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_auction_room(self, auction_pk):
        return AuctionRoom.objects.get(pk=auction_pk)

    @database_sync_to_async
    def add_participant(self):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        room.auction_paticipants.add(self.scope["user"])
        room.paticipant_count += 1
        room.save()

    @database_sync_to_async
    def remove_participant(self):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        room.auction_paticipants.remove(self.scope["user"])
        room.paticipant_count -= 1
        room.save()

    @database_sync_to_async
    def update_bid_price(self, new_bid):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        room.auction_bid_price = new_bid
        room.save()

    @database_sync_to_async
    def add_message(self, username, message):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        AuctionMessage.objects.create(
            auction_room=room,
            auction_bid_price=room.auction_bid_price,
            auction_user=self.scope["user"],
            auction_message=message,
        )

    @database_sync_to_async
    def add_bid_message(self, username, bid):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        AuctionMessage.objects.create(
            auction_room=room,
            auction_bid_price=bid,
            auction_user=self.scope["user"],
            auction_message=f"{username}님이 {bid}원을 입찰하셨습니다.",
        )

    @database_sync_to_async
    def add_join_message(self, username):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        AuctionMessage.objects.create(
            auction_room=room,
            auction_bid_price=room.auction_bid_price,
            auction_user=self.scope["user"],
            auction_message=f"{username}님이 입장하셨습니다.",
        )

    @database_sync_to_async
    def add_error_message(self, message):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        AuctionMessage.objects.create(
            auction_room=room,
            auction_bid_price=room.auction_bid_price,
            auction_user=self.scope["user"],
            auction_message=message,
        )

    @database_sync_to_async
    def add_message_message(self, username, message):
        room = AuctionRoom.objects.get(pk=self.auction_pk)
        AuctionMessage.objects.create(
            auction_room=room,
            auction_bid_price=room.auction_bid_price,
            auction_user=self.scope["user"],
            auction_message=f"{username} : {message}",
        )
