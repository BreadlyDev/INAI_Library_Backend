from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User, Group
from .serializers import UserSerializer, LoginSerializer, GroupSerializer


# def create_group(serializer: LoginSerializer):
#
#     serializer.


def get_all_users() -> User:
    return User.objects.all()


def get_user_by_field(field: str, value: str | int) -> User | None:
    field_kw: dict = {field: value}
    return User.objects.filter(**field_kw)


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


def create_token(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = {
        "access_token": str(access),
        "refresh_token": str(refresh)
    }

    return response


def create_user(request) -> dict:

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


def enter_system(request) -> dict:

    data = request.data
    # serializer = LoginSerializer(request.data)
    # serializer.is_valid(raise_exception=True)

    email, password = get_request_field_values(data, ["email", "password"])
    user = get_user_by_field(field="email", value=email)
    # serializer = UserSerializer(user)

    invalid = check_user_and_password(user, password)

    if invalid:
        return invalid

    tokens = create_token(user)

    return {
        "message": "User logged in successfully",
        **tokens,
        # **serializer.data
    }
