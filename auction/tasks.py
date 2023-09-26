from celery import shared_task
from datetime import datetime
from django.utils import timezone

from .models import AuctionRoom
from product.models import Products


@shared_task
def check_and_create_auction_rooms():
    # 현재 시간과 가까운 auction_start_at을 가진 Products 항목 조회
    # 현재 시간이 지난 상품들 중 아직 AuctionRoom이 생성되지 않은 것만 선택
    products_to_start = Products.objects.filter(
        auction_start_at__lte=timezone.now(),
        auction_room__isnull=True,
        product_active=True,
    )

    for product in products_to_start:
        # 새로운 AuctionRoom 생성
        AuctionRoom.objects.create(
            auction_host=product.seller_id,
            auction_room_name=product,
            auction_active=True,  # 경매 활성화 상태로 설정
        )

print("1")