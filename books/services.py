from django.http import FileResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import Book, Subcategory, Category
from .serializers import BookSerializer, CategorySerializer, SubcategorySerializer
from services.services import deserialize_data
from main.settings import ERROR_404_IMAGE


def create__book(request):
    result = deserialize_data(request, serialized_class=BookSerializer)
    return {
        "message": "Book was successfully added",
        **result
    }


def update__book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.image != request.data["image"] \
            and book.image.path != ERROR_404_IMAGE:
        default_storage.delete(book.image.path)
    result = deserialize_data(request, model=book, serialized_class=BookSerializer, partial=True)
    return {
        "message": f"Book with id {pk} was successfully updated",
        **result
    }


def delete__book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.image and book.image.path != ERROR_404_IMAGE:
        default_storage.delete(book.image.path)
    book.delete()
    return {"message": f"Book with id {pk} was successfully deleted"}


def get__book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)

    image_path = book.image.name
    if default_storage.exists(image_path):
        default_storage.url(image_path)
    else:
        book.image = ERROR_404_IMAGE
        book.save()

    return serializer.data


def get__all__books(request):
    books = get_list_or_404(Book)

    category = request.GET.get("category")
    less_orders = request.GET.get("less_orders")
    more_orders = request.GET.get("more_orders")
    author = request.GET.get("author")
    title = request.GET.get("title")

    if category:
        books = Book.objects.filter(category__title=category.capitalize())
    if less_orders:
        books = Book.objects.filter(orders__lte=less_orders)
    if more_orders:
        books = Book.objects.filter(orders__gte=more_orders)

    if author:
        books = Book.objects.filter(Q(author__icontains=author))
    elif title:
        books = Book.objects.filter(Q(title__icontains=title))

    serializer = BookSerializer(books, many=True)
    return serializer.data


def get_e_book_file(request, pk):
    file = get_object_or_404(Book, pk=pk)
    path = file.e_book.path
    response = FileResponse(open(path, 'rb'))
    response["Content-Disposition"] = f"attachment; filename = {file.e_book.name}"
    return response


def create__category(request):
    result = deserialize_data(request, serialized_class=CategorySerializer)
    return {
        "message": "Category was successfully added",
        **result
    }


def update__category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    result = deserialize_data(request, model=category,
                              serialized_class=CategorySerializer, partial=True)
    return {
        "message": f"Book with id {pk} was successfully updated",
        **result
    }


def delete__category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return {"message": f"Category with id {pk} was successfully deleted"}


def get__category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return serializer.data


def get__all__categories(request):
    categories = get_list_or_404(Category)
    serializer = CategorySerializer(categories, many=True)
    return serializer.data


def create__subcategory(request):
    result = deserialize_data(request, serialized_class=SubcategorySerializer)
    return {
        "message": "Subcategory was successfully added",
        **result
    }


def update__subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    result = deserialize_data(request, model=subcategory,
                              serialized_class=SubcategorySerializer, partial=True)
    return {
        "message": f"Subcategory with id {pk} was successfully updated",
        **result
    }


def delete__subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    subcategory.delete()
    return {"message": "Subcategory was successfully deleted"}


def get__subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    serializer = SubcategorySerializer(subcategory)
    return serializer.data


def get__all__subcategories(request):
    subcategories = get_list_or_404(Subcategory)
    serializer = SubcategorySerializer(subcategories, many=True)
    return serializer.data
