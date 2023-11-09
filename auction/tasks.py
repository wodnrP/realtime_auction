from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import AuctionRoom
from product.models import Products



@shared_task
def check_and_create_auction_rooms():
    # 현재 시간과 가까운 auction_start_at을 가진 Products 항목 조회
    # 현재 시간이 지난 상품들 중 아직 AuctionRoom이 생성되지 않은 것만 선택
    products_to_start = Products.objects.filter(
        auction_start_at__lte=timezone.now(),
        product_active=True,
    )

    for product in products_to_start:
        # 새로운 AuctionRoom 생성
        try:
            auction_room_check = product.auction_room
            if auction_room_check.auction_end_at <= timezone.now():
                auction_room_check.auction_active = False
                auction_room_check.save()
                product.product_active = False
                product.save()
            
        except:
            #product 등록 시 auction_end_at을 지정하지 않았다면 default값으로 설정
            if not product.auction_end_at:
                AuctionRoom.objects.create(
                    auction_host=product.seller_id,
                    auction_room_name=product,
                    auction_active=True  # 경매 활성화 상태로 설정
                )
            else:
                AuctionRoom.objects.create(
                    auction_host=product.seller_id,
                    auction_room_name=product,
                    auction_end_at = product.auction_end_at,
                    auction_active=True
                )
                

    return 'check auction'