from rest_framework import serializers
from .models import Order, OrderBook


class OrderBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBook
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()
    books = OrderBookSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_owner_email(self, instance):
        return instance.owner.email if instance.owner else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["owner"] = self.get_owner_email(instance)
        return representation


class LibrarianOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("status", "due_time")
