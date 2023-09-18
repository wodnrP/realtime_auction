from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from user.models import User
from product.models import Products


"""
auction_users : 경매 물건을 파는 사람 == 채팅방 주인
auction_product_name : 경매 제품 이름(경매 채팅방 이름) // 제품 당 1개의 채팅방만 생성가능(1:1)
auction_start_at : 경매 시작 시간
auction_end_at : 경매 마감 시간(user가 경매를 종료 했을 경우 마감 시간이 설정 됨)
auction_participants : 경매 참여자 (경매에 참여하는 사람)
auction_final_buyer : 낙찰 받는 사람 (물건을 구매하는 사람)
auction_final_price : 낙찰 가격 (낙찰자가 구매하는 최종 구매 가격) / 경매가 시작될 때 경매 물품의 가격으로 초기화 / 경매가 진행될 때마다 최고가로 업데이트
"""


class Auction(models.Model):
    auction_user = models.ForeignKey(
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
    auction_end_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="경매 마감 시간",
    )
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
    auction_final_price = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="경매 최종 가격",
    )

    @receiver(post_save, sender=Products)
    def update_auction_final_price(sender, instance, **kwargs):
        # Products 모델의 product_price가 변경될 때마다 연결된 Auction 모델의 auction_final_price 업데이트
        try:
            auction = Auction.objects.get(auction_product_name=instance)
            auction.auction_final_price = instance.product_price
            auction.save()
        except Auction.DoesNotExist:
            # Auction 객체가 없으면 생성
            Auction.objects.create(
                auction_product_name=instance,
                auction_final_price=instance.product_price,
            )

    def __str__(self):
        return f"주최자: {self.auction_user}, 경매 물품: {self.auction_product_name}, 낙찰자: {self.auction_final_buyer}, 최종 낙찰 가격: {self.auction_final_price}"

    def close_auction(self):
        """
        판매자가 경매를 마감한 시간을 경매 마감시간으로 설정합니다.
        """
        self.auction_end_at = timezone.now()
        self.save()

    class Meta:
        ordering = ["-auction_start_at"]
