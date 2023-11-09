from django.contrib import admin
from penalty.models import Penalty, BuyPenaltyReason, SellPenaltyReason


admin.site.register(Penalty)
admin.site.register(BuyPenaltyReason)
admin.site.register(SellPenaltyReason)
