from rest_framework.decorators import api_view
from .services import (get_all_books, get_book_by_id, get_books_by_cat,
                       create_book, update_book, delete_book)
from users.views import base_view


@api_view(["GET"])
def get_books(request):
    return base_view(request, get_all_books)


@api_view(["GET"])
def get_book_by_pk(request, pk: int):
    return base_view(request, get_book_by_id, pk)


@api_view(["GET"])
def get_book_by_pk(request, category: str):
    return base_view(request, get_book_by_id, category)


@api_view(["GET", "PUT", "DELETE"])
def change_book(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get_book_by_id, field=pk)
        case "PUT":
            return base_view(request, update_book, field=pk)
        case "DELETE":
            return base_view(request, delete_book, field=pk)
