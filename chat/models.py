from django.db import models
from user.models import User
from auction.models import AuctionRoom
# Create your models here.
class Chatting(models.Model):
    auction_id=models.OneToOneField(
        AuctionRoom,
        on_delete=models.CASCADE,
        verbose_name="연결된 경매"
    )
    
    def __str__(self):
        return str(self.auction_id)

class Message(models.Model):
    chatting_id=models.ForeignKey(
        Chatting, 
        on_delete=models.CASCADE,
        verbose_name="1:1 채팅방",
    )
    sender_id=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="메세지 발신자",
    )
    message_content=models.TextField(
        max_length=200,
        verbose_name="메세지 내용",
    )
    message_time=models.DateTimeField(
        auto_now_add=True,
        verbose_name="전송 시간",
    )

    class Meta:
        ordering = ["-message_time"]
