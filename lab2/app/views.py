from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Operation, Calculation, OperationCalculation


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


def delete_calculation(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE calculations SET status=5 WHERE id = %s", [calculation_id])

    return redirect("/")


def calculation(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return redirect("/")

    calculation = Calculation.objects.get(id=calculation_id)
    if calculation.status == 5:
        return redirect("/")
    
    operations = calculation.get_operations()
    for operation in operations:
         operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

    context = {
        "calculation": calculation,
        "operations": operations
    }

    # for operation in calculation.get_operations():
    #     operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"
    #     context['operation'] = operation # Добавьте operation в контекст

    return render(request, "calculation_page.html", context)


def get_draft_calculation():
    return Calculation.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()