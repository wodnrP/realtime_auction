from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User


class Penalty(models.Model):
    class PeanaltyTypeChoice(models.TextChoices):
        BUY = "buy", "구매"
        SELL = "sell", "판매"

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    penalty_type = models.CharField(max_length=4, choices=PeanaltyTypeChoice.choices)
    penalty_content = models.TextField()
    penalty_date = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender="penalty.Penalty")
    def update_user_access(sender, instance, created, **kwargs):
        if created:
            user = User.objects.get(id=instance.user_id.id)
            buy_penalty = Penalty.objects.filter(
                user_id=instance.user_id.id, penalty_type="buy"
            ).count()
            sell_penalty = Penalty.objects.filter(
                user_id=instance.user_id.id, penalty_type="sell"
            ).count()
            # user.can_buy가 true이고, 패널티의 개수가 3개 이상일 때 구매 불가 상태로 변경
            if instance.penalty_type == "buy":
                if user.can_buy & (buy_penalty >= 3):
                    user.can_buy = False

            # user.can_sell가 true이고, 패널티의 개수가 3개 이상일 때 판매 불가 상태로 변경
            elif instance.penalty_type == "sell":
                if user.can_sell & (sell_penalty >= 3):
                    user.can_sell = False

            user.save()
