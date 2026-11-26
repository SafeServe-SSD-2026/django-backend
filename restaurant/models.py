from functools import cached_property

from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator, \
    RegexValidator
from django.db import models

class Category(models.TextChoices):
    APPETIZER = 'APP', 'Appetizer'
    FIRST_COURSE = 'FIR', 'First Course'
    MAIN_COURSE = 'MAI', 'Main Course'
    DESSERT = 'DES', 'Dessert'
    DRINK = 'DRI', 'Drink'

class Table(models.Model):
    number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )

class Order(models.Model):
    table = models.OneToOneField(Table, on_delete=models.PROTECT, related_name='order')
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )

    @property
    def total(self):
        return sum(i.dish.price * i.quantity for i in self.items.select_related('dish'))

class Dish(models.Model):
    name = models.CharField(
        validators=[MinLengthValidator(3), MaxLengthValidator(50), RegexValidator(r"^[A-Za-z0-9 '\-]+$")]
    )
    category = models.CharField(max_length=3, choices=Category.choices)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999)])
    available = models.BooleanField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['order', 'dish'], name='unique_dish_per_order')]