from celery import shared_task
from .models import AuctionRoom
from payment.models import Payments


@shared_task
def create_payment_for_auction_winner(room_id):
    try:
        # AuctionRoom을 가져옴
        room = AuctionRoom.objects.get(pk=room_id)
        
        # Payment 모델에 필요한 정보를 설정
        payment = Payments(
            buyer=room.auction_winner,
            product_name=room.auction_room_name,
            payment_type="null",
            total_price=room,
            paid=False  
        )

        payment.save()

        room.payment_active = True
        room.save()

        return f'Payment created for Auction Room {room_id}'
    except AuctionRoom.DoesNotExist:
        return f'Auction Room with ID {room_id} does not exist'