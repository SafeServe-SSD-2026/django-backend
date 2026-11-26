from django.shortcuts import render
from rest_framework import viewsets

from restaurant.models import Table, Order, OrderItem, Dish
from restaurant.serializers import TableSerializer, OrderSerializer, DishSerializer, OrderItemSerializer, \
    OrderWriteSerializer


# Create your views here.

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__dish')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return OrderWriteSerializer
        return OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = OrderItemSerializer