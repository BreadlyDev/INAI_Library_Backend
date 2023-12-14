from .models import Book, Subcategory, Category
from .serializers import BookSerializer
from users.services import get_all_objects, get_objects_by_field, get_request_field_values
from services.services import serialize_data, deserialize_data


def create_book(request) -> dict | None:
    result = deserialize_data(request, serialized_class=BookSerializer)
    return result


def update_book(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk).first()
    result = deserialize_data(request, model=book, serialized_class=BookSerializer, partial=True)
    return result


def delete_book(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk).first()
    if not book:
        return {"message": "Book doesn't exist"}
    book.delete()
    return {"message": "Book was successfully deleted"}


def get_book_by_id(request, pk) -> dict | None:
    book = get_objects_by_field(model=Book, field="pk", value=pk)
    result = serialize_data(model=book, serialized_class=BookSerializer)
    if not book:
        return {"message": "Book doesn't exist"}
    return result


def get_all_books(request) -> dict | None:
    book = get_all_objects(Book)
    result = serialize_data(model=book, serialized_class=BookSerializer, many=True)
    return result


def get_books_by_cat(request, category) -> dict | None:
    book = get_objects_by_field(model=Book, field="category", value=category)
    result = serialize_data(model=book, serialized_class=BookSerializer, many=True)
    return result
