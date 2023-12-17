from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Review
from .serializers import ReviewSerializer
from services.services import deserialize_data


def create__review(request):
    result = deserialize_data(request, serialized_class=ReviewSerializer)
    # book = result["book"]
    return {
        "message": "Your review was successfully created",
        **result
    }
    # return result


def update__review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.author:
        result = deserialize_data(request, model=review,
                                  serialized_class=ReviewSerializer, partial=True)
        return {
            "message": f"Review with id {pk} was successfully updated",
            **result
        }
    return {"message": "You don't have permission to delete this review"}


def delete__review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.author:
        review.delete()
        return {"message": f"Review with id {pk} was successfully deleted"}
    return {"message": "You don't have permission to delete this review"}


def get__review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(review)
    return serializer.data


def get__all__reviews(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewSerializer(reviews, many=True)
    return serializer.data
