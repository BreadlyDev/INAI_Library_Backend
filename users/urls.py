from django.urls import path
from .views import register, login, logout, get_users, create_group, change_group

urlpatterns = [
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("users/list", get_users),
    path("group/create", create_group),
    path("group/<int:pk>", change_group),
]
