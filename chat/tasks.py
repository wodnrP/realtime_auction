from celery import shared_task
from datetime import datetime
from django.utils import timezone
from .models import AuctionRoom, Chatting

@shared_task
def create_chatting_for_completed_auctions():
    completed_auctions = AuctionRoom.objects.filter(
        auction_winner__isnull=False,
        auction_end_at__lt=timezone.now(),
        auction_active=False
    )

    for auction in completed_auctions:
        # 이미 생성된 Chatting 레코드가 있는지 확인
        existing_chatting = Chatting.objects.filter(auction_id=auction.id).first()
        
        # Chatting 레코드가 없는 경우 생성 
        if not existing_chatting:
            Chatting.objects.create(auction_id=auction)

    return 'check chat'
