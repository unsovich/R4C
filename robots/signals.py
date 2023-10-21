from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models import signals
from orders.models import Order
from .models import Robot


@receiver(signals.post_save, sender=Robot)
def send_new_robot_mail(sender, instance, created, **kwargs):
    print('signal send')   # тестируем работу сигнала

    if created:
        earliest_order = Order.objects.filter(robot_serial=instance.serial, status='Ожидает производства').order_by(
            'created').first()
        if earliest_order:
            customer = earliest_order.customer
            customer_email = customer.email
            # Отправить уведомление
            subject = 'Робот произведен'
            message = (f'Добрый день! \n Недавно вы интересовались нашим роботом модели {instance.model}, '
                       f'версии {instance.version}. \n '
                       f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.')
            from_email = 'robot@robot.com'
            recipient_list = [customer_email]
            send_mail(subject, message, from_email, recipient_list)
