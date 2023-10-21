from django.db import models
from customers.models import Customer
from robots.models import Robot


class Order(models.Model):
    STATUS_CHOICES = [
        ('Ожидает производства', 'Ожидает производства'),
        ('Заказ размещен', 'Заказ размещен'),
        ('В производстве', 'В производстве'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ожидает производства')  # добавил поле для статуса заказа

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"Order {self.id} for Robot {self.robot_serial}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    robot = models.ForeignKey(Robot, related_name='order_items', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
