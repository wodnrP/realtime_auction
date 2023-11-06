import re
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from penalty.models import Penalty, BuyPenaltyReason, SellPenaltyReason


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["auth_number", "is_admin"]

    def validate(self, data):
        is_password = re.compile(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$"
        )
        if not is_password.fullmatch(data["password"]):
            raise serializers.ValidationError("최소 8자리/영문,특수문자,숫자를  모두 포함해주세요")

        return data

    def update(self, instance, validated_data):
        if "password" in validated_data:
            is_password = re.compile(
                r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$"
            )
            if not is_password.fullmatch(validated_data["password"]):
                raise serializers.ValidationError("최소 8자리/영문,특수문자,숫자를  모두 포함해주세요")

            instance.set_password(validated_data.get("password", instance.password))
            instance.save()

        if "username" in validated_data:
            instance.username = validated_data.get("username", instance.username)
            instance.save()

        if "nickname" in validated_data:
            if validated_data["nickname"] == "":
                instance.nickname = f"user{instance.id}"
                instance.save()
            else:
                instance.nickname = validated_data.get("nickname", instance.nickname)
                instance.save()

        if "address" in validated_data:
            instance.address = validated_data.get("address", instance.address)
            instance.save()

        if "profile_image" in validated_data:
            instance.profile_image = validated_data.get(
                "profile_image", instance.profile_image
            )
            instance.save()

        return instance


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]

    def validate(self, data):
        is_phone_number = re.compile(r"010\d{4}\d{4}$")

        if not is_phone_number.fullmatch(data["phone_number"]):
            raise serializers.ValidationError("핸드폰 번호는 '-' 없이 번호만 작성해주세요.")

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 마지막에 받은 패널티 시간 3일 후 제약 해제
        if not user.can_buy:
            penalty = Penalty.objects.prefetch_related('buypenaltyreason_set').get(user_id=user)
            if penalty.buypenaltyreason_set.last().penalty_date + timedelta(seconds=30) <= timezone.now():
                user.can_buy = True
                
        if not user.can_sell:
            enalty = Penalty.objects.prefetch_related('sellpenaltyreason_set').get(user_id=user)
            if penalty.sellpenaltyreason_set.last().penalty_date + timedelta(days=3) <= timezone.now():
                user.can_sell = True
        user.save()
        
        token = super().get_token(user)
        token["phone_number"] = user.phone_number
        return token

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            self.fail('bad_token')