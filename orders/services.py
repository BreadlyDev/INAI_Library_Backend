from django.shortcuts import get_object_or_404, get_list_or_404
from services.services import deserialize_data, try_except_decorator
from .serializers import OrderSerializer, LibrarianOrderSerializer
from .models import Order


# def create__order(request):
#     result = deserialize_data(request, serialized_class=OrderSerializer, owner=request.user)
#     return result

@try_except_decorator
def create__order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=request.user)
    return serializer.data


def update__order(request, pk):
    order = get_object_or_404(OrderSerializer, pk=pk)
    result = deserialize_data(request, model=order, serialized_class=LibrarianOrderSerializer, partial=True)
    return result


def delete__order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return {"message": f"Order with id {pk} was successfully deleted"}


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
