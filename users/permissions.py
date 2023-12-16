from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from .models import User, ROLES


# ACCESS_DENIED = "You don't have a permission to do it"


# def is_admin(user: User):
#     if user.role != ROLES[0][1]:
#         return Response({"message", ACCESS_DENIED}, status=status.HTTP_403_FORBIDDEN)


# def is_librarian(user: User):
#     if user.role != ROLES[1][1]:
#         return Response({"message", ACCESS_DENIED}, status=status.HTTP_403_FORBIDDEN)


# def is_librarian(user: User):
#     if user == AnonymousUser:
#         return {"message": "Unauthorized users can't do that"}
#     if user.role != ROLES[1][1]:
#         return {"message", ACCESS_DENIED}

def is_admin(user: User):
    if user.role != ROLES[0][1]:
        return False
    return True


def is_authenticated(user: User):
    if not user.is_authenticated:
        return False
    return True


def is_librarian(user: User):
    if user.role != ROLES[2][1]:
        return False
    return True


def is_student(user: User):
    if user.role != ROLES[2][1]:
        return False
    return True


def not_student(user: User):
    if user.role == ROLES[1][1]:
        return False
    return True
