from django.urls import path
from .views import register, login, logout, get_users, create_group, change_group

urlpatterns = [
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("list/users", get_users),
    path("create/group", create_group),
    path("change/group/<int:pk>", change_group),
]
