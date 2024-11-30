from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from app.models import Operation, Calculation, OperationCalculation

from math import factorial, gcd


def index(request):
    operation_name = request.GET.get("operation_name", "")
    operations = Operation.objects.filter(status=1)

    if operation_name:
        operations = operations.filter(name__icontains=operation_name)

    draft_calculation = get_draft_calculation()

    context = {
        "operation_name": operation_name,
        "operations": operations
    }
    for operation in operations:
         operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

    if draft_calculation:
        context["operations_count"] = len(draft_calculation.get_operations())
        context["draft_calculation"] = draft_calculation

    return render(request, "operations_page.html", context)


def add_operation_to_draft_calculation(request, operation_id):
    operation = Operation.objects.get(pk=operation_id)

    draft_calculation = get_draft_calculation()

    if draft_calculation is None:
        draft_calculation = Calculation.objects.create()
        draft_calculation.owner = get_current_user()
        draft_calculation.date_created = timezone.now()
        draft_calculation.save()


    if OperationCalculation.objects.filter(calculation=draft_calculation, operation=operation).exists():
        return redirect("/")

    item = OperationCalculation(
        calculation=draft_calculation,
        operation=operation
    )
    item.save()

    return redirect("/")


def operation_details(request, operation_id):

    operation = Operation.objects.get(id=operation_id)
    operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"
    
    context = {
        "operation": operation
    }

    return render(request, "operation_page.html", context)

def calculation(request, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    calculation_priority = request.GET.get("calculation_priority", "")
    calculation_creator = request.GET.get("calculation_creator", "")
    if calculation.status == 2 or calculation.status > 3:
        return redirect("/")

    operations = calculation.get_operations()
    for operation in operations:
        operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

    context = {
        "calculation": calculation,
        "operations": operations,
        "calculation_priority": calculation_priority,
        "calculation_creator": calculation_creator,
    }
    return render(request, "calculation_page.html", context)

def delete_calculation(request, calculation_id):
    if request.method == 'POST':
        calculation = get_object_or_404(Calculation, pk=calculation_id)
        # new_calculation_priority = request.POST.get('calculation_priority', '').strip()
        # new_calculation_creator = request.POST.get('calculation_creator', '').strip()

        # Обновление поля `value` для связанных записей OperationCalculation
        # related_operations = OperationCalculation.objects.filter(calculation_id=calculation_id)

        # # Обновление записи Calculation
        # calculation.calculation_creator = new_calculation_creator
        # calculation.priority = new_calculation_priority
        calculation.status = 2
        calculation.date_complete = timezone.now()
        calculation.save()

        return redirect("/")
    else:
        return redirect("/")
    
from django.http import JsonResponse

def process_operations(request, calculation_id):
    if request.method == 'POST':
        calculation = get_object_or_404(Calculation, pk=calculation_id)
        new_calculation_priority = request.POST.get('calculation_priority', '').strip()
        new_calculation_creator = request.POST.get('calculation_creator', '').strip()

        # Получаем все операции, связанные с вычислением
        operations = calculation.get_operations()

        for operation in operations:
            # Получаем значение из поля для данной операции
            field_name = f"operation_{operation.id}"
            input_value = request.POST.get(field_name, '').strip()

            if not input_value.isdigit():
                return render(
                    request, 
                    'error_page.html', 
                    {'error': f'Введите корректное число для операции {operation.name}'}
                )

            input_value = int(input_value)

            # Выполняем расчет
            if operation.number is None:  # Факториал
                result = factorial(input_value)
            else:  # НОД
                result = gcd(operation.number, input_value)

            # Обновляем значение в связанной таблице OperationCalculation
            operation_calc, created = OperationCalculation.objects.get_or_create(
                calculation=calculation,
                operation=operation
            )
            operation_calc.value = result
            operation_calc.save()
        
        calculation.calculation_creator = new_calculation_creator
        calculation.priority = new_calculation_priority
        calculation.status = 3
        calculation.date_formation = timezone.now()
        calculation.save()

        
        # Возвращаемся на страницу после обработки
        # return redirect(request.META.get('HTTP_REFERER', '/'))
        return redirect("/")

    return redirect("/")



def get_draft_calculation():
    #return Calculation.objects.filter(status=1).first()
    return Calculation.objects.filter(status__in=[1, 3]).first()




def get_current_user():
    return User.objects.filter(is_superuser=False).first()