import json
from django.core.exceptions import ObjectDoesNotExist

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chatting, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chatting_pk"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # 로그인 된 사용자만 채팅 참여
        if not self.user.is_authenticated:
            await self.close()

        # 채팅방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.chat_message("경매가 완료되어 1:1 채팅이 시작되었습니다.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.send_message(message)
        await self.crete_or_update_chat_message(
            self.user, self.room_name, message
        )

    # 1:1 채팅 메세지
    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    # 채팅 시작 메세지 
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {   
                    "type": "send_message",
                    "message": event,
                }
            )
        )

    # 채팅 내용 저장
    @database_sync_to_async
    def crete_or_update_chat_message(self, user, room_name, message):
        try:
            chat_room = Chatting.objects.filter(auction_id=room_name)
            if chat_room.exists():
                chat_message = Message.objects.filter(
                    chatting_id=chat_room[0], 
                    sender_id=user,
                    message_content=message,
                )

                if not chat_message.exists():
                    new_chat_message = Message.objects.create(
                        chatting_id=chat_room[0],
                        sender_id=user,
                        message_content=message,
                    )
                    new_chat_message.save()
                    return True
        
        except ObjectDoesNotExist:
            return None