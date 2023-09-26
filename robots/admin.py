from django.contrib import admin
from .models import Robot


@admin.register(Robot)  # регистрация роботов в админ-панель
class RobotAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'model', 'version', 'quantity']
    list_filter = ['is_active', 'model']
