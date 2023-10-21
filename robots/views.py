from io import BytesIO
import xlsxwriter
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .forms import ProductionReportForm
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


def create_excel_report(robots, start_date, end_date):
    excel_data = BytesIO()  # байтовый объект для хранения xlsx-файла
    wb = xlsxwriter.Workbook(excel_data, {'in_memory': True})  # рабочая книга xlsx

    for robot in robots:  # лист для каждой модели
        model = robot['model']
        version = robot['version']
        count = robot['count']

        ws = wb.get_worksheet_by_name(model)  # получаем лист с именем модели
        if ws is None:  # если такого листа нет, создаем его
            ws = wb.add_worksheet(model)
            header_format = wb.add_format({  # формат заголовков таблицы
                'bold': True,
                'align': 'center',
                'valign': 'vcenter'
            })
            data_format = wb.add_format({  # формат данных в столбцах "Модель" и "Версия"
                'align': 'center',
                'valign': 'vcenter'
            })
            # Записываем заголовки таблицы и применяем формат
            headers = ["Модель", "Версия", f"Произведено за {start_date} - {end_date}"]
            for col_num, header in enumerate(headers):
                ws.write(0, col_num, header, header_format)
                ws.set_column(col_num, col_num, len(header) + 2)  # задаем ширину колонки
        # Записываем модель, версию и количество на лист
        row_number = ws.dim_rowmax + 1
        ws.write(row_number, 0, model, data_format)
        ws.write(row_number, 1, version, data_format)
        ws.write(row_number, 2, count)

    wb.close()  # сохраняем книгу

    return excel_data


def generate_report(request):
    if request.method == 'POST':
        form = ProductionReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            robots = Robot.objects.filter(
                created__range=(start_date, end_date)
            ).values('model', 'version').annotate(count=Count('id'))

            context = {'form': form, 'robots': robots}
            return render(request, 'report.html', context)

    else:
        form = ProductionReportForm()

    context = {'form': form}
    return render(request, 'report.html', context)


def download_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    robots = Robot.objects.filter(
        created__range=(start_date, end_date)
    ).values('model', 'version').annotate(count=Count('id'))

    excel_data = create_excel_report(robots, start_date, end_date)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=robot_production_report.xlsx'
    response.write(excel_data.getvalue())

    return response
