from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)


@receiver(pre_save, sender=Robot)  # авто-генерация (pre_save) serial перед сохранением записи Robot
def generate_serial(sender, instance, **kwargs):
    if not instance.serial:  # Генерировать serial если пустой
        instance.serial = f"{instance.model}-{instance.version}"
