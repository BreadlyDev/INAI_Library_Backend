from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User, Group
from .serializers import UserSerializer


def get_all_users() -> User:
    return User.objects.all()


def get_user_by_id(_id: int) -> User:
    return User.objects.filter(id=_id)


def create_token(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = {
        "access_token": str(access),
        "refresh_token": str(refresh)
    }

    return response


def create_user(serializer: UserSerializer) -> dict:

    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    tokens = create_token(user)

    response = {
        "message": "User registered successfully",
        "user": serializer.validated_data,
        **tokens
    }
    return response
