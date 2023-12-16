from django.shortcuts import get_object_or_404, get_list_or_404
from services.services import deserialize_data
from .serializers import OrderSerializer, LibrarianOrderSerializer
from .models import Order


def create__order(request):
    result = deserialize_data(request, serialized_class=OrderSerializer)
    return result


def update__order(request, pk):
    order = get_object_or_404(OrderSerializer, pk=pk)
    result = deserialize_data(request, model=order, serialized_class=LibrarianOrderSerializer, partial=True)
    return result


def delete__order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return {"message": "Order was successfully deleted"}


def get__order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order)
    return serializer.data


def get__all__orders(request):
    orders = get_list_or_404(Order)
    serializer = OrderSerializer(orders, many=True)
    return serializer.data


def get__own__orders(request):
    orders = Order.objects.filter(owner=request.user)
    serializer = OrderSerializer(orders, many=True)
    return serializer.data
