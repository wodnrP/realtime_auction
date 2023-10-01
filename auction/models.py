from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from datetime import timedelta
from user.models import User
from product.models import Products


class AuctionRoom(models.Model):
    auction_host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_host",
        verbose_name="물건 판매자",
    )
    auction_room_name = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        related_name="auction_room",
        verbose_name="경매 물품",
    )
    auction_final_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="경매 최종 가격",
    )
    auction_winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auction_winner",
        verbose_name="경매 최종 낙찰자",
    )
    auction_paticipants = models.ManyToManyField(
        User,
        blank=True,
        related_name="auction_paticipants",
        verbose_name="경매 참여자들",
    )

    paticipant_count = models.PositiveIntegerField(
        default=0,
        verbose_name="경매 참여자 수",
    )
    auction_end_at = models.DateTimeField(
        default=timezone.now()+timedelta(minutes=30),
    )
    auction_active = models.BooleanField(
        default=False, verbose_name="경매 활성화 여부"
    )  # 경매 시작 시 True, 경매 종료 시 False

    def save(self, *args, **kwargs):
        # 경매 종료 시간이 경매 시작 시간보다 빠를 경우, 에러를 발생시킵니다.
        if (
            self.auction_end_at
            and self.auction_start_at
            and self.auction_end_at < self.auction_start_at
        ):
            raise ValueError("경매 종료 시간은 경매 시작 시간보다 빠를 수 없습니다.")

        # 경매가 종료되었을 경우, 경매 활성화 여부를 False로 설정합니다.
        if self.auction_end_at and timezone.now() > self.auction_end_at:
            self.auction_active = False
        super(AuctionRoom, self).save(*args, **kwargs)


    @property
    def starting_price(self):
        return self.auction_room_name.product_price

    @property
    def auction_start_at(self):
        return self.auction_room_name.auction_start_at

    @property
    def product_active(self):
        return self.auction_room_name.product_active

    class Meta:
        verbose_name = "경매 채팅 방"
        verbose_name_plural = "경매 채팅 방"

    def __str__(self):
        return f"경매 채팅방 : {self.auction_room_name}"


class AuctionMessage(models.Model):
    auction_room = models.ForeignKey(
        AuctionRoom,
        on_delete=models.CASCADE,
        related_name="auction_room",
        verbose_name="경매 채팅방",
    )
    auction_bid_price = models.PositiveIntegerField(
        default=0,
        verbose_name="경매 제시 가격",
    )
    auction_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="message_user",
        verbose_name="경매 채팅 참가자",
    )
    auction_message = models.TextField(
        max_length=100,
        verbose_name="경매 채팅 메세지",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="메시지 전송 시간",
    )

    class Meta:
        verbose_name = "경매 채팅 메세지"
        verbose_name_plural = "경매 채팅 메세지"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"경매 채팅방 :{self.auction_room}의 최종 가격 : {self.auction_bid_price}"