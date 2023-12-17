from rest_framework import serializers
from .models import Review
from books.models import Book


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
