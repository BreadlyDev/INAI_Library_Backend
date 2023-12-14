from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer, LoginSerializer
from services.services import (get_all_objects, get_objects_by_field,
                               get_request_field_values, serialize_data, deserialize_data,
                               try_except_decorator)


def check_user_and_password(user: User, password) -> dict | None:
    if not user:
        return {"message": "User doesn't exist"}
    if not user.check_password(password):
        return {"message": "Invalid password"}


def check_refresh_token(refresh_token: RefreshToken) -> dict | None:
    if not refresh_token:
        return {"message": "Refresh token doesn't exist"}


@try_except_decorator
def create_token(user: User) -> dict | None:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    response = {
        "access_token": str(access),
        "refresh_token": str(refresh)
    }
    return response


@try_except_decorator
def create_user(request) -> dict | None:
    result, user = deserialize_data(request, UserSerializer, return_model=True)
    result["group"] = result["group"].title
    tokens = create_token(user)
    response = {
        "message": "User registered successfully",
        **result,
        **tokens
    }
    return response


@try_except_decorator
def enter_system(request) -> dict | None:
    data = request.data
    email, password = get_request_field_values(data, ["email", "password"])
    user = get_objects_by_field(model=User, field="email", value=email).first()
    result = serialize_data(user, LoginSerializer)
    invalid = check_user_and_password(user, password)
    if invalid:
        return invalid
    tokens = create_token(user)
    response = {
        "message": "User logged in successfully",
        **tokens,
        **result
    }
    return response


@try_except_decorator
def quit_system(request) -> dict | None:
    data = request.data
    refresh_token = get_request_field_values(data, ["refresh_token"])
    invalid = check_refresh_token(*refresh_token)
    if invalid:
        return invalid
    RefreshToken(*refresh_token).blacklist()
    response = {"message": "User logged out successfully "}
    return response


@try_except_decorator
def get_all_users(request) -> dict | None:
    users = get_objects_by_field(model=User, field="is_superuser", value=False)
    result = serialize_data(model=users, serialized_class=UserSerializer, many=True)
    return result


@try_except_decorator
def add_group(request) -> dict | None:
    result = deserialize_data(request, serialized_class=GroupSerializer)
    response = {
        "message": "Group registered successfully",
        **result,
    }
    return response


@try_except_decorator
def get_all_groups(request) -> dict | None:
    group = get_all_objects(model=Group)
    result = serialize_data(model=group, serialized_class=GroupSerializer, many=True)
    return result


@try_except_decorator
def get_group_by_id(request, field) -> dict | None:
    group = get_objects_by_field(model=Group, field="pk", value=field).first()
    result = serialize_data(model=group, serialized_class=GroupSerializer)
    return result


@try_except_decorator
def update_group(request, pk) -> dict | None:
    group = get_objects_by_field(model=Group, field="pk", value=pk).first()
    if not group:
        return {"message": "Group not found"}
    result = deserialize_data(request, serialized_class=GroupSerializer, partial=True)
    return result


@try_except_decorator
def delete_group(request, pk) -> dict | None:
    group = get_objects_by_field(model=Group, field="pk", value=pk).first()
    if not group:
        return {"message": "Group not found"}
    group.delete()
    return {"message": "Group was successfully deleted"}
