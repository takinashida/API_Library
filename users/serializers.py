from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password

class  UserSerializer(serializers.ModelSerializer):
    # payments=serializers.SerializerMethodField()

    class Meta:
        model= User
        fields = ["email", "password", "telegram_chat_id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        hash_password = make_password(password)
        validated_data["password"] = hash_password
        instance = User(**validated_data)
        instance.save()
        return instance

    # def get_payments(self, obj):
    #     return PaymentSerializer(obj.payment.filter, many=True ).data