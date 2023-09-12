import re

from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]

    def validate(self, data):
        is_phone_number = re.compile(r"010\d{4}\d{4}$")

        if not is_phone_number.fullmatch(data["phone_number"]):
            raise serializers.ValidationError("핸드폰 번호는 '-' 없이 번호만 작성해주세요.")

        return data
