import json
from typing import Set

from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin,
    action,
)

from .models import Auction, AuctionMessage
from .serializers import AuctionSerializer, AuctionMessageSerializer
from user.models import User
from user.serializers import UserSerializer


class AuctionConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    lookup_field = "pk"

    async def connect(self):
        # 1. 경매 객체 가져오기
        auction_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.auction = await self.get_auction_by_pk(auction_pk)

        # 2. 사용자 인증 (예: 로그인 된 사용자인지 확인)
        user = self.scope["user"]
        if not user.is_authenticated:
            return await self.close()

        # 3. WebSocket 그룹에 연결
        auction_group_name = f"auction_{self.auction.pk}"
        await self.channel_layer.group_add(auction_group_name, self.channel_name)
        self.groups.append(auction_group_name)

        # 4. 연결 수락
        await self.accept()

    async def disconnect(self, code):
        # 1. 사용자가 경매 참가자 목록에 있으면 제거
        if hasattr(self, "auction"):
            await self.remove_user_from_auction(self.auction)
            await self.notify_auction_users()

        # 2. WebSocket 그룹에서 연결 제거
        auction_group_name = f"auction_{self.auction.pk}"
        await self.channel_layer.group_discard(auction_group_name, self.channel_name)

        # 3. 부모 클래스의 disconnect 메서드 호출
        await super().disconnect(code)

    @action()
    async def leave_auction(self, pk, **kwargs):
        await self.remove_user_from_auction(pk)

    @action()
    async def create_message(self, message, **kwargs):
        auction: Auction = await self.get_object(pk=self.auction_participants)
        created_message = await database_sync_to_async(AuctionMessage.objects.create)(
            auction_room=auction,
            user=self.scope["user"],
            auction_bid_price=message["auction_bid_price"],
            auction_message_content=message["auction_message_content"],
        )

        # 경매의 최종 가격이 업데이트 될 때만 알림 발송
        if created_message.auction_bid_price > (auction.auction_final_price or 0):
            auction.auction_final_price = created_message.auction_bid_price
            await database_sync_to_async(auction.save)(
                update_fields=["auction_final_price"]
            )

            # 알림 발송
            await self.channel_layer.group_send(
                f"auction__{auction.pk}",
                {
                    "type": "auction.price.update",
                    "price": auction.auction_final_price,
                },
            )

    @action()
    async def subscribe_to_messages_in_auction(self, pk, request_id, **kwargs):
        await self.message_activity.subscribe(auction=pk, request_id=request_id)

    @model_observer(AuctionMessage)
    async def message_activity(
        self, message, observer=None, subscribing_request_ids=[], **kwargs
    ):
        for request_id in subscribing_request_ids:
            message_body = dict(
                request_id=request_id, **AuctionMessageSerializer(message).data
            )
            message_body.update({"type": "message"})
            await self.send_json(message_body)

    @message_activity.groups_for_signal
    def message_activity(self, instance: AuctionMessage, **kwargs):
        yield f"auction__{instance.auction_room.pk}"
        yield f"pk__{instance.pk}"

    @message_activity.groups_for_consumer
    def message_activity(self, auction=None, **kwargs):
        if auction is not None:
            yield f"auction__{auction.pk}"

    @message_activity.serializer
    def message_activity(self, instance: AuctionMessage, action, **kwargs):
        return dict(
            data=AuctionMessageSerializer(instance).data,
            action=action.value,
            pk=instance.pk,
        )

    async def notify_auction_users(self):
        auction: Auction = await self.get_object(pk=self.auction_participants)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    "type": "auction.update",
                    "event": "update",
                    "usuarios": await self.auction_participants(auction),
                    "data": AuctionSerializer(auction).data,
                },
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({"usuarios": event["usuarios"]}))

    @database_sync_to_async
    def get_auction_by_pk(self, pk) -> Auction:
        return Auction.objects.get(pk=pk)

    @database_sync_to_async
    def get_object(self, pk: int) -> Auction:
        return Auction.objects.get(pk=pk)

    @database_sync_to_async
    def participants(self, auction: Auction):
        return [
            UserSerializer(user).data for user in auction.auction_participants.all()
        ]

    @database_sync_to_async
    def remove_user_from_auction(self, auction):
        user: User = self.scope["user"]
        user.auctions_participants.remove(auction)

    @database_sync_to_async
    def add_user_to_auction(self, pk):
        user: User = self.scope["user"]
        if not user.auctions_participants.filter(pk=self.auction_participants).exists():
            user.auctions_participants.add(Auction.objects.get(pk=pk))
