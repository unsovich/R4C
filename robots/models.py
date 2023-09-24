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


class ProductionReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    robot_model = models.CharField(max_length=2)
    robot_version = models.CharField(max_length=2)
    total_production = models.PositiveIntegerField()

    @staticmethod
    def generate_report(start_date, end_date, robot_model, robot_version):
        total_production = Robot.objects.filter(
            model=robot_model, version=robot_version,
            created__gte=start_date, created__lte=end_date
        ).count()
        return total_production

    def __str__(self):
        return (f"Отчет о производстве {self.robot_model} ({self.robot_version}) "
                f"за период с {self.start_date} по {self.end_date}")
