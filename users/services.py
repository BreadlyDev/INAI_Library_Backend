from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer, LoginSerializer
from services.services import (get_all_objects, deserialize_data, try_except_decorator)


def check_user_and_password(user: User, password) -> dict | None:
    if not user:
        return {"message": "User doesn't exist"}
    if not user.check_password(password):
        return {"message": "Invalid password"}


def check_refresh_token(refresh_token: RefreshToken) -> dict | None:
    if not refresh_token:
        return {"message": "Refresh token doesn't exist"}


@try_except_decorator
def create_token(user) -> dict | None:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = {
        "access_token": str(access),
        "refresh_token": str(refresh)
    }

    return response


@try_except_decorator
def create_user(request, *args, **kwargs) -> dict | None:
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    tokens = create_token(user)

    response = {
        "message": "User registered successfully",
        **serializer.data,
        **tokens
    }

    return response


@try_except_decorator
def enter_system(request, *args, **kwargs) -> dict | None:
    password = request.data["password"]
    user = get_object_or_404(User, email=request.data["email"])
    serializer = LoginSerializer(user)
    invalid = check_user_and_password(user, password)

    if invalid:
        return invalid

    tokens = create_token(user)
    response = {
        "message": "User logged in successfully",
        **tokens,
        **serializer.data
    }

    return response


@try_except_decorator
def quit_system(request, *args, **kwargs) -> dict | None:
    refresh_token = request.data["refresh_token"]
    invalid = check_refresh_token(refresh_token)

    if invalid:
        return invalid

    RefreshToken(refresh_token).blacklist()
    response = {"message": "User logged out successfully"}
    return response


@try_except_decorator
def get_all_users(request, *args, **kwargs) -> dict | None:
    users = get_list_or_404(User, is_superuser=False)
    serializer = UserSerializer(users, many=True)
    return serializer.data


@try_except_decorator
def add_group(request, *args, **kwargs) -> dict | None:
    result = deserialize_data(request, serialized_class=GroupSerializer)
    response = {
        "message": "Group registered successfully",
        **result,
    }
    return response


@try_except_decorator
def get__all__groups(request, *args, **kwargs) -> dict | None:
    group = get_list_or_404(Group)
    serializer = GroupSerializer(group, many=True)
    return serializer.data


@try_except_decorator
def get_group_by_id(request, *args, **kwargs) -> dict | None:
    group = get_object_or_404(Group, *args, **kwargs)
    serializer = GroupSerializer(group)
    return serializer.data


@try_except_decorator
def update_group(request, pk) -> dict | None:
    group = get_object_or_404(Group, pk=pk)
    result = deserialize_data(request, model=group, serialized_class=GroupSerializer, partial=True)
    return result


@try_except_decorator
def delete_group(request, pk) -> dict | None:
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    return {"message": f"Group with id {pk} was successfully deleted"}
