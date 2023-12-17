from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Review
from .serializers import ReviewSerializer
from services.services import deserialize_data, try_except_decorator


def create__review(request):
    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)

    return {
        "message": "Your review was successfully created",
        **serializer.data
    }


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


def get__all__reviews(request, book_id: int):
    reviews = Review.objects.filter(book_id=book_id)
    serializer = ReviewSerializer(reviews, many=True)
    return serializer.data
