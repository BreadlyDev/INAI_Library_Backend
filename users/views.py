from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, GroupSerializer
from .services import create_user


@api_view(["POST"])
def register(request):
    try:
        user_data = create_user(serializer=UserSerializer(data=request.data))
        # return Response(user)
        print(user_data)
        return Response(user_data)
    except Exception as e:
        print(f"Error: {e}")
        raise