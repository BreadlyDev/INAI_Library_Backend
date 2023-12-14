from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import books.views as views

urlpatterns = [
    path("book/list", views.get_list_books),
    path("book/create", views.create_book),
    path("book/<int:pk>", views.crud_book),
    path("book/download/<int:pk>", views.get_e_book_file),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
