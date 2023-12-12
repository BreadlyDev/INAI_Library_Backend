from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, GroupSerializer
from .services import create_user, enter_system


def base_post_view(request, function, http_status: status):
    try:
        user_data = function(request)
        return Response(user_data, status=http_status)
    except Exception as e:
        return Response({"Error happened": e})


@api_view(["POST"])
def register(request):
    return base_post_view(request, create_user, status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    return base_post_view(request, enter_system, status.HTTP_200_OK)
