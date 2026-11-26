from django.db import transaction
from rest_framework import serializers

from restaurant.models import Table, Dish, OrderItem, Order


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number']

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'category', 'price', 'available']

class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source='dish.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'dish', 'dish_name', 'quantity']

    def validate_dish(self, dish):
        if not dish.available:
            raise serializers.ValidationError('Dish not available')
        return dish

    def create(self, validated_data):
        with transaction.atomic():
            item = (OrderItem.objects.select_for_update()
                    .filter(order=validated_data['order'], dish=validated_data['dish'])
                    .first()
                    )
            if item is None:
                return OrderItem.objects.create(**validated_data)

            new_quantity = item.quantity + validated_data['quantity']
            if new_quantity > 50:
                raise serializers.ValidationError(
                    {'quantity': 'Total quantity for this dish cannot exceed 50'})
            item.quantity = new_quantity
            item.save()
            return item

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'seats', 'items', 'total']

class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table', 'seats']