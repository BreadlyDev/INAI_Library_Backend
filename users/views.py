from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import (create_user, enter_system, quit_system,
                       get_all_users, add_group, get_group_by_id, update_group, delete_group)


def base_view(request, function, field=None):
    try:
        if field:
            object_data = function(request, field=field)
            return Response(object_data)
        object_data = function(request)
        return Response(object_data)
    except Exception as e:
        return Response({"Error happened": e})


@api_view(["POST"])
def register(request):
    return base_view(request, create_user)


@api_view(["POST"])
def login(request):
    return base_view(request, enter_system)


@api_view(["POST"])
def logout(request):
    return base_view(request, quit_system)


@api_view(["GET"])
def get_users(request):
    return base_view(request, get_all_users)


@api_view(["POST"])
def create_group(request):
    return base_view(request, add_group)


@api_view(["GET", "PUT", "DELETE"])
def change_group(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get_group_by_id, field=pk)
        case "PUT":
            return base_view(request, update_group, field=pk)
        case "DELETE":
            return base_view(request, delete_group, field=pk)
