from django.contrib import admin
from .models import Robot


# регистрируем роботов в админ-панель для возможности манипуляций с ними
@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ['serial', 'model', 'version', 'created']
    list_filter = ['serial', 'model']
