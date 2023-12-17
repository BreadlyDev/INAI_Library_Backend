from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services.services import base_view
from users.permissions import is_librarian, is_authenticated
from .services import (get__all__reviews, get__review, create__review,
                       update__review, delete__review)


@api_view(["GET"])
def get_all_reviews(request, book_id: int):
    return base_view(request, get__all__reviews, book_id=book_id)


@api_view(["POST"])
def create_review(request):
    if not is_authenticated(request.user):
        return Response({"message": "You are not authenticated"}, status.HTTP_403_FORBIDDEN)
    if is_librarian(request.user):
        return Response({"message": "You can't make orders"}, status.HTTP_403_FORBIDDEN)
    return base_view(request, create__review)


@api_view(["GET", "PUT", "DELETE"])
def crud_review(request, pk: int):
    if request.method in ["PUT", "PATCH", "DELETE"]:
        if not is_authenticated(request.user):
            return Response({"message": "You are not authenticated"}, status.HTTP_403_FORBIDDEN)
    match request.method:
        case "GET":
            return base_view(request, get__review, pk=pk)
        case "PUT":
            return base_view(request, update__review, pk=pk)
        case "DELETE":
            return base_view(request, delete__review, pk=pk)
