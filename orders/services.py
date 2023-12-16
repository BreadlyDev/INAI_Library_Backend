from django.shortcuts import get_object_or_404, get_list_or_404
from services.services import deserialize_data
from .serializers import OrderSerializer, LibrarianOrderSerializer
from .models import Order


def create__book(request):
    result = deserialize_data(request, serialized_class=OrderSerializer)
    return result


def update__book(request, pk):
    order = get_object_or_404(OrderSerializer, pk=pk)
    result = deserialize_data(request, model=order, serialized_class=LibrarianOrderSerializer, partial=True)
    return result


def delete__book(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return {"message": "Order was successfully deleted"}


def get__book(request, pk):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order)
    return serializer.data


def get__all__books(request):
    orders = get_list_or_404(Order)
    serializer = OrderSerializer(orders, many=True)
    return serializer.data
