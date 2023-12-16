from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("book/all", views.get_all_books),
    path("book/create", views.create_book),
    path("book/<int:pk>", views.crud_book),
    path("book/download/<int:pk>", views.get_e_book_file),
    path("category/all", views.get_all_categories),
    path("category/create", views.create_category),
    path("category/<int:pk>", views.crud_category),
    path("subcategory/all", views.get_all_subcategories),
    path("subcategory/create", views.create_subcategory),
    path("subcategory/<int:pk>", views.crud_subcategory),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
