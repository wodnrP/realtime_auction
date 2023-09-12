from djongo import models
from user.models import User
from auction.models import Auction 
# Create your models here.
class Chatting(models.Model):
    auction_id=models.ForeignKey(Auction,on_delete=models.CASCADE)

    class Message(models.Model):
        sender_id=models.ForeignKey(User,on_delete=models.CASCADE)
        message_type=models.TextField()
        message_content=models.TextField()

        class Meta:
            abstract=True

    messages=models.ArrayModelField(model_container=Message,)
