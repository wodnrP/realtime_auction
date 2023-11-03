from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from auction.models import AuctionRoom
from penalty.models import Penalty


@shared_task
def check_and_give_buy_penalty():
    # 매일 자정 상품의 결제 상태 체크
    not_paid_auction_rooms = AuctionRoom.objects.filter(
        auction_active=False, payment_active=True
    )

    for room in not_paid_auction_rooms:
        # 경매가 끝난 후 3일이 지나도 payment_active가 true인 경우 패널티 부여
        if timezone.now() > room.auction_room_name.auction_end_at + timedelta(days=3):
            Penalty.objects.create(
                user_id=room.auction_winner,
                penalty_type="buy",
                penalty_content=f"{room.auction_room_name} 기간 안에 결제를 하지 않았습니다.",
            )
            room.payment_active = False
            room.save()

    return "check buy penalty"
