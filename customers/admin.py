from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email']
