from django.db import models
from user.models import User
from auction.models import Auction 
# Create your models here.
class Chatting(models.Model):
    auction_id=models.ForeignKey(Auction,on_delete=models.CASCADE)

class Message(models.Model):
    chatting_id=models.ForeignKey(Chatting, on_delete=models.CASCADE)
    sender_id=models.ForeignKey(User,on_delete=models.CASCADE)
    message_type=models.TextField()
    message_content=models.TextField()