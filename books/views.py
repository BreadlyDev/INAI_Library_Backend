from rest_framework.decorators import api_view
from services.services import base_view
from .services import (get__all__books, get__book, create__book,
                       update__book, delete__book, get_e_book_file,
                       get__all__categories, get__category, create__category,
                       update__category, delete__category, get__all__subcategories,
                       get__subcategory, create__subcategory, update__subcategory,
                       delete__subcategory)


@api_view(["GET"])
def get_all_books(request):
    return base_view(request, get__all__books)


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


@api_view(["GET"])
def get_all_categories(request):
    return base_view(request, get__all__categories)


@api_view(["POST"])
def create_category(request):
    return base_view(request, create__category)


@api_view(["GET", "PUT", "DELETE"])
def crud_category(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get__category, pk=pk)
        case "PUT":
            return base_view(request, update__category, pk=pk)
        case "DELETE":
            return base_view(request, delete__category, pk=pk)


@api_view(["GET"])
def get_all_subcategories(request):
    return base_view(request, get__all__subcategories)


@api_view(["POST"])
def create_subcategory(request):
    return base_view(request, create__subcategory)


@api_view(["GET", "PUT", "DELETE"])
def crud_subcategory(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get__subcategory, pk=pk)
        case "PUT":
            return base_view(request, update__subcategory, pk=pk)
        case "DELETE":
            return base_view(request, delete__subcategory, pk=pk)