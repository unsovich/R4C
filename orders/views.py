from django.db import transaction
from django.core.mail import send_mail
from django.shortcuts import render
from orders.forms import OrderForm
from robots.models import Robot


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            robot_serial = form.cleaned_data['robot_serial']
            current_user_email = request.user.email

            with transaction.atomic():  # операции блока выполняются как единое целое: ошибка -> откат
                try:
                    robots = Robot.objects.select_for_update().filter(serial=robot_serial)
                    if robots.exists():
                        robot = robots.first()  # первый робот из набора
                except Robot.DoesNotExist:
                    robot = None

                # создание заказа
                order = form.save(commit=False)
                order.customer_email = current_user_email
                order.robot_serial = robot_serial

                if robot and robot.quantity > 0:
                    # робот доступен, уменьшаем остаток роботов и устанавливаем статус заказа
                    robot.quantity -= 1
                    robot.save()
                    order.status = 'Заказ размещен'
                else:
                    # робот не найден или = 0
                    order.status = 'Ожидает производства'

                order.save()

                if order.status.startswith('Заказ'):
                    subject = f'Успешный заказ № {order.id}'
                    message = f'Ваш заказ № {order.id} был успешно размещен.'
                else:
                    subject = f'Предзаказ № {order.id} принят'
                    message = (f'Ваш предзаказ № {order.id} был принят. Вы будете уведомлены, '
                               f'как только робот будет произведен.')

                # уведомление клиенту
                from_email = 'robot@robot.com'
                recipient_list = [current_user_email]
                send_mail(subject, message, from_email, recipient_list)

                return render(request,
                              'orders/created.html',
                              {'order_status': order.status})

    else:
        form = OrderForm()

    context = {'form': form}
    return render(request, 'orders/create.html', context)
