import re

from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['auth_number','is_admin']
    
    def validate(self,data):
        is_password = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$')
        if not is_password.fullmatch(data["password"]):
            raise serializers.ValidationError("최소 8자리/영문,특수문자,숫자를  모두 포함해주세요")

        return data
        

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]

    def validate(self, data):
        is_phone_number = re.compile(r"010\d{4}\d{4}$")

        if not is_phone_number.fullmatch(data["phone_number"]):
            raise serializers.ValidationError("핸드폰 번호는 '-' 없이 번호만 작성해주세요.")

        return data
