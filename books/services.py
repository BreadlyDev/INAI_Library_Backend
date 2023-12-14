from django.http import FileResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Book, Subcategory, Category
from .serializers import BookSerializer
from services.services import deserialize_data


def create__book(request) -> dict | None:
    result = deserialize_data(request, serialized_class=BookSerializer)
    return result


def update__book(request, pk) -> dict | None:
    book = get_object_or_404(Book, pk=pk)
    result = deserialize_data(request, model=book, serialized_class=BookSerializer, partial=True)
    return result


def delete__book(request, pk) -> dict | None:
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return {"message": "Book was successfully deleted"}


def get__book(request, pk) -> dict | None:
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return serializer.data


def get__all__books(request, *args, **kwargs) -> dict | None:
    book = get_list_or_404(Book, *args, **kwargs)
    category = request.GET.get("category")
    if category:
        book = Book.objects.filter(category__title=category.capitalize())
    serializer = BookSerializer(book, many=True)
    return serializer.data


def get_books_by_cat(request, category) -> dict | None:
    book = get_list_or_404(Book, category=category)
    serializer = BookSerializer(book, many=True)
    return serializer.data


def get_e_book_file(request, pk):
    file = get_object_or_404(Book, pk=pk)
    path = file.e_book.path
    response = FileResponse(open(path, 'rb'))
    response["Content-Disposition"] = f"attachment; filename = {file.e_book.name}"
    response["Content-Type"] = "application/msword"
    return response
