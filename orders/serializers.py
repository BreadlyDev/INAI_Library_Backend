from rest_framework import serializers
from .models import Order, OrderBook
from books.models import Book


class OrderBookSerializer(serializers.ModelSerializer):
    order = serializers.ReadOnlyField()
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = OrderBook
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()
    books = OrderBookSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_owner_email(self, instance):
        return instance.owner.email if instance.owner else None

    def create(self, validated_data):
        books_data = validated_data.pop("books")
        order = Order.objects.create(**validated_data)

        for book_data in books_data:
            OrderBook.objects.create(order=order, **book_data)

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["owner"] = self.get_owner_email(instance)
        return representation


class LibrarianOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("status", "due_time")
