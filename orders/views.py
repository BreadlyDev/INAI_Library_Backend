from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from services.services import base_view
from users.permissions import is_librarian, is_authenticated
from .services import (get__all__orders, get__order, create__order,
                       update__order, delete__order, get__own__orders)

@api_view(["GET"])
def get_all_orders(request):
    if not is_authenticated(request.user):
        return Response({"message": "You are not authenticated"}, status.HTTP_403_FORBIDDEN)
    if not is_librarian(request.user):
        return base_view(request, get__own__orders)
        # return Response({"message": "You don't have permission"}, status.HTTP_403_FORBIDDEN)
    return base_view(request, get__all__orders)


@api_view(["POST"])
def create_order(request):
    if not is_authenticated(request.user):
        return Response({"message": "You are not authenticated"}, status.HTTP_403_FORBIDDEN)
    if is_librarian(request.user):
        return Response({"message": "You can't make orders"}, status.HTTP_403_FORBIDDEN)
    return base_view(request, create__order)


@api_view(["GET", "PUT", "DELETE"])
def crud_order(request, pk: int):
    if not is_authenticated(request.user):
        return Response({"message": "You are not authenticated"}, status.HTTP_403_FORBIDDEN)
    match request.method:
        case "GET":
            return base_view(request, get__order, pk=pk)
        case "PUT":
            return base_view(request, update__order, pk=pk)
        case "DELETE":
            return base_view(request, delete__order, pk=pk)
