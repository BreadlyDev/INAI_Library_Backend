from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, logout, get_users, create_group, crud_group

urlpatterns = [
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("users/all", get_users),
    path("group/create", create_group),
    path("group/<int:pk>", crud_group),
    path('activate/refresh/token', TokenRefreshView.as_view()),
]
