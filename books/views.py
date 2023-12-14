from rest_framework.decorators import api_view
from .services import (get__all__books, get__book, create__book,
                       update__book, delete__book, get_e_book_file)
from users.views import base_view


@api_view(["GET"])
def get_list_books(request, *args, **kwargs):
    return base_view(request, get__all__books, *args, **kwargs)


@api_view(["GET"])
def download_e_book(request, pk: int):
    return get_e_book_file(request, pk=pk)


@api_view(["POST"])
def create_book(request):
    return base_view(request, create__book)


@api_view(["GET", "PUT", "DELETE"])
def crud_book(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get__book, pk=pk)
        case "PUT":
            return base_view(request, update__book, pk=pk)
        case "DELETE":
            return base_view(request, delete__book, pk=pk)
