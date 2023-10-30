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
            payment_date="null",
            total_price=room,
            paid=False  # 이 값을 설정하여 결제가 완료된 것으로 표시
        )

        payment.save()

        return f'Payment created for Auction Room {room_id}'
    except AuctionRoom.DoesNotExist:
        return f'Auction Room with ID {room_id} does not exist'