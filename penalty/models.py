from djongo import models

from user.models import User

class Penalty(models.Model):
    user_id = models.ForeignKey(User,  on_delete=models.CASCADE)
    buy_penalty = models.IntegerField()
    buy_penalty_content = models.CharField(max_length=255)
    sell_penalty = models.IntegerField()
    sell_penalty_content = models.CharField(max_length=255)