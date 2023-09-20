from celery import shared_task
from datetime import datetime, timedelta
from .models import Auction


@shared_task
def update_auction_active_status():
    # 현재 시간을 기준으로 시작된지 1분 이내의 Auction을 활성화
    just_started_auctions = Auction.objects.filter(
        auction_start_at__lte=datetime.now(),
        auction_start_at__gte=datetime.now() - timedelta(minutes=1),
        active=False,
    )
    just_started_auctions.update(active=True)

    # 현재 시간을 기준으로 종료된지 1분 이내의 Auction을 비활성화
    just_ended_auctions = Auction.objects.filter(
        auction_end_at__lte=datetime.now(),
        auction_end_at__gte=datetime.now() - timedelta(minutes=1),
        active=True,
    )
    just_ended_auctions.update(active=False)
