from rest_framework import serializers
from .models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.username = user.email
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
        return user
