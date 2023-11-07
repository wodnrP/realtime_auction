from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = "__all__"
