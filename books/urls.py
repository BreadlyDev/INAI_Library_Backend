from django.urls import path
from . import views

urlpatterns = [
    path("book/list", views.get_books),
    path("book/create", views.get_book_by_pk),
    path("book/<int:pk>", views.change_book),
]
