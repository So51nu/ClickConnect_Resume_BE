from rest_framework import serializers
from .models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "name",
            "email",
            "pincode",
            "-created_at",
        ]


class OTPSendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=6)
