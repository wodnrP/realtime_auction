import json
from django.core.exceptions import ObjectDoesNotExist

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chatting, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["auction_pk"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # 로그인 된 사용자만 채팅 참여
        if not self.user.is_authenticated:
            await self.close()

        host = await self.get_chat_room()

        if not host:
            await self.close()
        else:
            self.host = host

        # 채팅방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.chat_message("경매가 완료되어 1:1 채팅이 시작되었습니다.")
        await self.enter_or_exit_room("enter")

    async def disconnect(self, close_code):
        await self.enter_or_exit_room("exit")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.chat_message(message)

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def crete_or_update_chat_message(self, user, room_name):
        try:
            chat_room = Chatting.objects.filter(pk=room_name)
            if chat_room.exists():
                chat_message = Message.objects.filter(
                    chatting_id=chat_room[0], 
                    sender_id=user,
                )

                if not chat_message.exists():
                    new_chat_message = Message.objects.create(
                        chatting_id=chat_room[0],
                        sender_id=user,
                    )
                    new_chat_message.save()
                    return True
        
        except ObjectDoesNotExist:
            return None