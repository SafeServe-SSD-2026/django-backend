from django.contrib import admin
from restaurant.models import Table, Order, Dish, OrderItem

# Register your models here.

admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Dish)
admin.site.register(OrderItem)
