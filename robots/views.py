from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Robot
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат данных.'}, status=400)

        model = data.get('model')
        version = data.get('version')
        created = data.get('created')

        try:
            validate_data(model, version)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        robot = Robot(model=model, version=version, created=created)
        robot.save()

        return JsonResponse({'message': 'Робот успешно создан'}, status=201)
    else:
        return JsonResponse({'error': 'Неверный метод запроса'}, status=405)


# Валидация данных
def validate_data(model, version):
    if len(model) != 2 or not model.isalnum():
        raise ValidationError(
            'Модель должна состоять из двух символов (буквы и цифры).',
            code='invalid_robot_data'
        )
    if len(version) != 2 or not version.isalnum():
        raise ValidationError(
            'Версия должна состоять из двух символов (буквы и цифры).',
            code='invalid_robot_data'
        )
