from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Review
from .serializers import ReviewSerializer
from services.services import deserialize_data


def create__review(request):
    result = deserialize_data(request, serialized_class=ReviewSerializer)
    return result


def update__review(request, pk):
    category = get_object_or_404(Review, pk=pk)
    result = deserialize_data(request, model=category,
                              serialized_class=ReviewSerializer, partial=True)
    return result


def delete__review(request, pk):
    category = get_object_or_404(Review, pk=pk)
    category.delete()
    return {"message": f"Review with id {pk} was successfully deleted"}


def get__review(request, pk):
    category = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(category)
    return serializer.data


def get__all__reviews(request):
    categories = get_list_or_404(Review)
    serializer = ReviewSerializer(categories, many=True)
    return serializer.data