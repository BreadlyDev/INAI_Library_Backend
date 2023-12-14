from .models import Book, Subcategory, Category
from .serializers import BookSerializer
from users.services import get_all_objects, get_objects_by_field, get_request_field_values


def create_book(request) -> dict | None:
    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data


def update_book(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk).first()
    serializer = BookSerializer(book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data


def delete_book(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk).first()

    if not book:
        return {"message": "Book doesn't exist"}

    book.delete()

    return {"message": "Book was successfully deleted"}


def get_book_by_id(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk)
    book_data = BookSerializer(book)

    if not book:
        return {"message": "Book doesn't exist"}

    return book_data.data


def get_all_books(request) -> dict | None:
    book = get_all_objects(Book)
    book_data = BookSerializer(book, many=True)

    return book_data.data


def get_books_by_cat(request, category) -> dict | None:
    book = get_objects_by_field(model=Book, field="category", value=category)
    book_data = BookSerializer(book, many=True)

    return book_data.data
