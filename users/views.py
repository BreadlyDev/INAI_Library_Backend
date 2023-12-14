from rest_framework.decorators import api_view
from .services import (create_user, enter_system, quit_system,
                       get_all_users, add_group, get_group_by_id, update_group, delete_group)
from services.services import base_view


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
def crud_group(request, pk: int):
    match request.method:
        case "GET":
            return base_view(request, get_group_by_id, pk=pk)
        case "PUT":
            return base_view(request, update_group, pk=pk)
        case "DELETE":
            return base_view(request, delete_group, pk=pk)
