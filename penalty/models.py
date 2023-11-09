from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User


class BuyPenaltyReason(models.Model):
    penalty_id = models.ForeignKey(Penalty, on_delete=models.CASCADE)
    penalty_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    @receiver(post_save, sender="penalty.BuyPenaltyReason")
    def update_user_access(sender, instance, created, **kwargs):
        if created:
            penalty = Penalty.objects.get(id=instance.penalty_id.id)
            penalty.buy_penalty += 1
            penalty.save()
            
            user = penalty.user_id
            if user.can_buy & (penalty.buy_penalty >= 3):
                user.can_buy = False
                user.save()


class SellPenaltyReason(models.Model):
    penalty_id = models.ForeignKey(Penalty, on_delete=models.CASCADE)
    penalty_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    @receiver(post_save, sender="penalty.SellPenaltyReason")
    def update_user_access(sender, instance, created, **kwargs):
        if created:
            penalty = Penalty.objects.get(id=instance.penalty_id.id)
            penalty.sell_penalty += 1
            penalty.save()

            user = penalty.user_id
            if user.can_sell & (penalty.sell_penalty >= 3):
                user.can_sell = False
                user.save()
