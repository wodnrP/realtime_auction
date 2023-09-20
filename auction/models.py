from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from user.models import User
from product.models import Products


"""
auction_host : 경매 물건을 파는 사람 == 채팅방 주인
auction_product_name : 경매 제품 이름(경매 채팅방 이름) // 제품 당 1개의 채팅방만 생성가능(1:1)
auction_start_at : 경매 시작 시간
auction_end_at : 경매 마감 시간(user가 경매를 종료 했을 경우 마감 시간이 설정 됨)
auction_participants : 경매 참여자 (경매에 참여하는 사람)
auction_final_buyer : 낙찰 받는 사람 (물건을 구매하는 사람)
auction_final_price : 낙찰 가격 (낙찰자가 구매하는 최종 구매 가격) / 경매가 시작될 때 경매 물품의 가격으로 초기화 / 경매가 진행될 때마다 최고가로 업데이트
"""


class Auction(models.Model):
    auction_host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="auctions_user",
        verbose_name="경매 주최자",
    )
    auction_product_name = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        related_name="auctions_product",
        verbose_name="경매 물품",
    )
    auction_start_at = models.DateTimeField(
        null=False,
        blank=False,
        # default=timezone.now,
        verbose_name="경매 시작 시간",
    )
    # auction_end_at = models.DateTimeField(
    #     blank=True,
    #     null=True,
    #     verbose_name="경매 마감 시간",
    # )
    auction_active = models.BooleanField(default=False, verbose_name="경매 활성화 상태")
    auction_participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="auctions_participants",
        verbose_name="경매 참여자",
    )
    auction_final_buyer = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auctions_final_buyer",
        verbose_name="경매 낙찰자",
    )
    auction_final_price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="경매 최종 가격",
    )

    @receiver(post_save, sender=Products)
    def update_auction_final_price(sender, instance, **kwargs):
        # Products 모델의 product_price가 변경될 때마다 연결된 Auction 모델의 auction_final_price 업데이트
        update_fields = kwargs.get("update_fields")
        try:
            auction = Auction.objects.get(auction_product_name=instance)
            if "product_price" in (update_fields if update_fields is not None else []):
                # 현재 낙찰가 보다 높은 가격으로만 업데이트
                if instance.product_price > (auction.auction_final_price or 0):
                    auction.auction_final_price = instance.product_price
                    auction.save(update_fields=["auction_final_price"])
        except Auction.DoesNotExist:
            # Auction의 객체가 없다면 생성
            if "product_price" in (update_fields if update_fields is not None else []):
                Auction.objects.create(
                    auction_host=instance.product_user,
                    auction_product_name=instance,
                    auction_final_price=instance.product_price,
                    # auction_start_at=instance.auction_start_at,
                    # auction_end_at=instance.auction_end_at,
                    active=False,
                )

    def __str__(self):
        return f"주최자: {self.auction_host}, 경매 물품: {self.auction_product_name}, 낙찰자: {self.auction_final_buyer}, 최종 낙찰 가격: {self.auction_final_price}"

    def close_auction(self, closing_price):
        """
        판매자가 경매를 마감할 때 호출되며, closing_price를 낙찰가격으로 설정합니다.
        """
        if closing_price > self.auction_final_price:
            self.auction_final_price = closing_price
            self.auction_end_at = timezone.now()
            self.save(update_fields=["auction_final_price", "auction_end_at"])

    class Meta:
        ordering = ["-auction_start_at"]


"""
sender_id : 보낸 메세지
auction_room : 채팅방(물건 이름)
auction_content : 채팅 설명
auction_message_type : 메세지 타입(문자열 / 이미지 / 파일)
auction_bid_price : 입찰 가격
auction_message_content : 메세지 내용
auction_timestamp : 채팅 시간
"""


class AuctionMessage(models.Model):
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    auction_room = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="auction_room_messages",
    )
    auction_message_type = models.TextField()
    auction_bid_price = models.IntegerField(blank=True, null=True, verbose_name="입찰 가격")
    auction_message_content = models.TextField()
    auction_timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def lastest_bid_price(cls, auction_room):
        """
        경매방의 마지막 입찰가를 반환합니다.
        """
        lastest_bid = (
            cls.objects.filter(
                auction_room=auction_room, auction_bid_price__isnull=False
            )
            .order_by("-auction_timestamp")
            .first()
        )
        return lastest_bid.auction_bid_price if lastest_bid else None