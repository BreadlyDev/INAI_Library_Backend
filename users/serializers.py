from rest_framework import serializers
from .models import User, Group


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        if password:
            user = super().create(validated_data)
            user.set_password(password)
            user.save()

            return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["group"] = instance.group.title if instance.group.title else None


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")
