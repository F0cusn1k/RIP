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
    operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"  # Добавьте полный URL
    
    context = {
        "operation": operation
    }
    
    # context = {
    #     "operation": Operation.objects.get(id=operation_id)
    # }

    return render(request, "operation_page.html", context)

def calculation(request, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    calculation_number = request.GET.get("calculation_number", "")
    calculation_creator = request.GET.get("calculation_creator", "")
    if calculation.status == 5:
        return redirect("/")

    operations = calculation.get_operations()
    for operation in operations:
        operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

    context = {
        "calculation": calculation,
        "operations": operations,
        "calculation_number": calculation_number,
        "calculation_creator": calculation_creator,
    }
    return render(request, "calculation_page.html", context)

def delete_calculation(request, calculation_id):
    if request.method == 'POST':
        calculation = get_object_or_404(Calculation, pk=calculation_id)
        new_calculation_number = request.POST.get('calculation_number', '').strip()
        new_calculation_creator = request.POST.get('calculation_creator', '').strip()
        
        if not new_calculation_number.isdigit():
            return render(request, 'error_page.html', {'error': 'Не введено корректное число для обработки'})
        
        new_calculation_number = int(new_calculation_number)

        # Обновление поля `value` для связанных записей OperationCalculation
        related_operations = OperationCalculation.objects.filter(calculation_id=calculation_id)

        for op_calc in related_operations:
            if op_calc.operation and op_calc.operation.id == 1:
                op_calc.value = factorial(new_calculation_number)
            elif op_calc.operation:
                op_calc.value = gcd(op_calc.operation.id, new_calculation_number)
            else:
                op_calc.value = None  # Если `operation` отсутствует, оставляем значение пустым
            op_calc.save()

        # Обновление записи Calculation
        calculation.calculation_creator = new_calculation_creator
        calculation.number = new_calculation_number
        calculation.status = 5
        calculation.save()

        return redirect("/")
    else:
        return redirect("/")

def get_draft_calculation():
    return Calculation.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()