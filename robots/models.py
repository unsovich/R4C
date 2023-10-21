from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0)  # добавил поле для количества доступных роботов
    is_active = models.BooleanField(default=True)  # чтобы включались неактивные в отчет о производстве

    def __str__(self):
        return f"{self.model} {self.version} ({self.serial})"

    def get_absolute_url(self):
        return reverse('robots:robot_detail', args=[self.id, self.model, self.version])


@receiver(pre_save, sender=Robot)  # авто-генерация serial перед сохранением робота
def generate_serial(sender, instance, **kwargs):
    if not instance.serial:  # генерировать serial если пустой
        instance.serial = f"{instance.model}-{instance.version}"
