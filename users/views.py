from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import (create_user, enter_system, quit_system,
                       get_all_users, add_group, get_group_by_id, update_group, delete_group)


def base_view(request, function, http_status: status, field=None):
    try:
        if field:
            user_data = function(request, field=field)
            return Response(user_data, status=http_status)
        user_data = function(request)
        return Response(user_data, status=http_status)
    except Exception as e:
        return Response({"Error happened": e})


@api_view(["POST"])
def register(request):
    return base_view(request, create_user, status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    return base_view(request, enter_system, status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    return base_view(request, quit_system, status.HTTP_200_OK)


@api_view(["GET"])
def get_users(request):
    return base_view(request, get_all_users, status.HTTP_200_OK)


@api_view(["POST"])
def create_group(request):
    return base_view(request, add_group, status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def change_group(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get_group_by_id, status.HTTP_200_OK, field=pk)
        case "PUT":
            return base_view(request, update_group, status.HTTP_200_OK, field=pk)
        case "DELETE":
            return base_view(request, delete_group, status.HTTP_200_OK, field=pk)
