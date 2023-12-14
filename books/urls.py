from django.urls import path
from . import views

urlpatterns = [
    path("list/book", views.get_books),
    path("create/book", views.get_book_by_pk),
    path("change/book/<int:pk>", views.change_book),
    path("change/book/<str:category>", views.get_books_by_cat),
]
