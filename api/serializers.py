from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Server, Member, Channel, Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # always write-only
    dob = serializers.DateField(
        required=False, allow_null=True,
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d']
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'display_name', 'dob', 'subscribe', 'password']

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        feilds = ['id', 'name', 'image_url', 'invite_code', 'owner']

    def create(self, validated_data):
        server = Server(**validated_data)
        server.save()

