from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer, LoginSerializer


def get_all_objects(model):
    return model.objects.all()


def get_objects_by_field(model, field: str, value: any):
    field_kw: dict = {field: value}
    return model.objects.filter(**field_kw)


def check_list_len(_list: list):
    if len(_list) == 0:
        raise ValueError("The list is empty")


def get_request_field_values(data: dict, fields: list[str]) -> list:
    data_list: list = []
    for field in fields:
        if not data.get(field):
            continue
        data_list.append(data.get(field))
    check_list_len(data_list)
    return data_list


def check_user_and_password(user: User, password) -> dict | None:
    if not user:
        return {"message": "User doesn't exist"}
    if not user.check_password(password):
        return {"message": "Invalid password"}



def check_refresh_token(refresh_token: RefreshToken) -> dict | None:
    if not refresh_token:
        return {"message": "Refresh token doesn't exist"}


def create_token(user: User) -> dict | None:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = {
        "access_token": str(access),
        "refresh_token": str(refresh)
    }

    return response


def create_user(request) -> dict | None:
    try:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group = serializer.validated_data["group"].title
        serializer.validated_data["group"] = group
        tokens = create_token(user)
        response = {
            "message": "User registered successfully",
            **serializer.validated_data,
            **tokens
        }
        return response
    except Exception as e:
        print(e)


def enter_system(request) -> dict | None:
    try:
        data = request.data
        email, password = get_request_field_values(data, ["email", "password"])
        user = get_objects_by_field(model=User, field="email", value=email).first()
        user_data = LoginSerializer(user)
        invalid = check_user_and_password(user, password)
        if invalid:
            return invalid
        tokens = create_token(user)
        response = {
            "message": "User logged in successfully",
            **tokens,
            **user_data.data
        }
        return response
    except Exception as e:
        print(e)


def quit_system(request) -> dict | None:
    try:
        data = request.data
        refresh_token = get_request_field_values(data, ["refresh_token"])
        invalid = check_refresh_token(*refresh_token)
        if invalid:
            return invalid
        RefreshToken(*refresh_token).blacklist()
        response = {
            "message": "User logged out successfully "
        }
        return response
    except Exception as e:
        print(e)


def get_all_users(request) -> dict | None:
    try:
        users = get_objects_by_field(model=User, field="is_superuser", value=False)
        serializer = UserSerializer(users, many=True)
        return serializer.data
    except Exception as e:
        print(e)


def add_group(request) -> dict | None:
    try:
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "Group registered successfully",
            **serializer.validated_data,
        }
        return response
    except Exception as e:
        print(e)


def get_all_groups(request) -> dict | None:
    try:
        group = get_all_objects(model=Group)
        serializer = GroupSerializer(group, many=True)
        return serializer.data
    except Exception as e:
        print(e)


def get_group_by_id(request, pk) -> dict | None:
    try:
        group = get_objects_by_field(model=Group, field="pk", value=pk).first()
        serializer = GroupSerializer(group)
        return serializer.data
    except Exception as e:
        print(e)


def update_group(request, pk) -> dict | None:
    try:
        data = request.data
        group = get_objects_by_field(model=Group, field="pk", value=pk).first()
        if not group:
            return {"message": "Group not found"}
        serializer = GroupSerializer(group, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    except Exception as e:
        print(e)


def delete_group(request, pk) -> dict | None:
    try:
        group = get_objects_by_field(model=Group, field="pk", value=pk).first()
        if not group:
            return {"message": "Group not found"}
        group.delete()
        return {"message": "Group was successfully deleted"}
    except Exception as e:
        print(e)
