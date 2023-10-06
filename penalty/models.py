from django.db import models

from user.models import User

class Penalty(models.Model):
    class PeanaltyTypeChoice(models.TextChoices):
        BUY = 'buy','구매'
        SELL = 'sell','판매'
    
    user_id = models.ForeignKey(User,  on_delete=models.CASCADE)
    penalty_type = models.CharField(max_length=4,choices=PeanaltyTypeChoice.choices)
    penalty_content = models.TextField()
    penalty_date = models.DateTimeField(auto_now_add=True)