from django.urls import path
from . import views

urlpatterns = [
    path("review/all", views.get_all_reviews),
    path("review/create", views.create_review),
    path("review/<int:pk>", views.crud_review),
]
