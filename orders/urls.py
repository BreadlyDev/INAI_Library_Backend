from django.urls import path
from . import views

urlpatterns = [
    path("order/all", views.get_all_orders),
    path("order/create", views.create_order),
    path("order/<int:pk>", views.crud_order),
]
