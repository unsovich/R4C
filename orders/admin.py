from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['robot']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'robot_serial', 'status', 'created']
    list_filter = ['created', 'status']
    list_editable = ['status']
    inlines = [OrderItemInline]
