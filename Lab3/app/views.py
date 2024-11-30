from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def search_operations(request):
    """
    Возвращает список всех операций и текущую заявку (calculation со статусом 1 или 3).
    """
    operation_name = request.GET.get("operation_name", "")
    operations = Operation.objects.all()

    if operation_name:
        operations = operations.filter(name__icontains=operation_name)

    # Находим текущую заявку (со статусом 1 или 3)
    current_calculation = Calculation.objects.filter(status__in=[1, 3]).first()

    data = {
        "operations": OperationSerializer(operations, many=True).data,
        "calculation": (
            CalculationSerializer(current_calculation).data if current_calculation else None
        )
    }

    return Response(data)


@api_view(["GET"])
def get_operation_by_id(request, operation_id):
    if not Operation.objects.filter(pk=operation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = Operation.objects.get(pk=operation_id)
    serializer = OperationSerializer(operation)
    return Response(serializer.data)


@api_view(["POST"])
def create_operation(request):
    serializer = OperationSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_operation(request, operation_id):
    if not Operation.objects.filter(pk=operation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = Operation.objects.get(pk=operation_id)
    serializer = OperationSerializer(operation, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
def update_operation_image(request, operation_id):
    try:
        operation = Operation.objects.get(id=operation_id)
        image = request.FILES.get('image')

        if not image:
            return Response({"error": "Image file is required."}, status=status.HTTP_400_BAD_REQUEST)

        operation.image = image
        operation.save()

        return Response(OperationSerializer(operation).data, status=status.HTTP_200_OK)
    except Operation.DoesNotExist:
        return Response({"error": "Operation not found."}, status=status.HTTP_404_NOT_FOUND)


# @api_view(["DELETE"])
# def delete_operation(request, operation_id):
#     if not Operation.objects.filter(pk=operation_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     operation = Operation.objects.get(pk=operation_id)
#     operation.delete()

#     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["DELETE"])
def delete_operation(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    operation.status = 2  # Меняем статус на "Удалена"
    operation.save()

    return Response(OperationSerializer(operation).data, status=status.HTTP_200_OK)

@api_view(["GET"])
def search_calculations(request):
    """
    Возвращает список всех заявок (calculations), независимо от статуса.
    """
    calculation_name = request.GET.get("calculation_name", "")
    calculations = Calculation.objects.all()

    if calculation_name:
        calculations = calculations.filter(name__icontains=calculation_name)

    # Формируем список с добавлением операций для каждой заявки
    data = [
        {
            **CalculationSerializer(calc).data,
            "operations": [
                OperationSerializer(op.operation).data
                for op in OperationCalculation.objects.filter(calculation=calc)
            ]
        }
        for calc in calculations
    ]

    return Response(data, content_type="application/json")

@api_view(["GET"])
def get_calculation_by_id(request, calculation_id):
    """
    Возвращает указанную заявку (со статусом 1 или 3) и все связанные операции.
    """
    calculation = get_object_or_404(Calculation, pk=calculation_id, status__in=[1, 3])

    data = {
        "calculation": CalculationSerializer(calculation).data,
        "operations": [
            OperationSerializer(op.operation).data
            for op in OperationCalculation.objects.filter(calculation=calculation)
        ]
    }

    return Response(data)


@api_view(["POST"])
def create_calculation(request):
    serializer = CalculationSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_calculation(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)
    serializer = CalculationSerializer(calculation, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
def update_status_user(request, calculation_id):
    try:
        calculation = Calculation.objects.get(id=calculation_id)

        if 'status' not in request.data:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        calculation.status = request.data['status']
        calculation.save()

        return Response(CalculationSerializer(calculation).data, status=status.HTTP_200_OK)
    except Calculation.DoesNotExist:
        return Response({"error": "Calculation not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_status_admin(request, calculation_id):
    try:
        calculation = Calculation.objects.get(id=calculation_id)

        if 'status' not in request.data:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        calculation.status = request.data['status']
        calculation.save()

        return Response(CalculationSerializer(calculation).data, status=status.HTTP_200_OK)
    except Calculation.DoesNotExist:
        return Response({"error": "Calculation not found."}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(["DELETE"])
# def delete_calculation(request, calculation_id):
#     if not Calculation.objects.filter(pk=calculation_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     calculation = Calculation.objects.get(pk=calculation_id)

#     if calculation.status != 1:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     calculation.status = 5
#     calculation.save()

#     serializer = CalculationSerializer(calculation, many=False)

#     return Response(serializer.data)

@api_view(["DELETE"])
def delete_calculation(request, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)

    if calculation.status not in [1, 3]:  # Проверяем, можно ли менять статус
        return Response({"detail": "Cannot delete this calculation."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    calculation.status = 2  # Меняем статус на "Удалена"
    calculation.save()

    return Response(CalculationSerializer(calculation).data, status=status.HTTP_200_OK)



@api_view(["POST"])
def add_operation_to_calculation(request, operation_id, calculation_id):
    if not Operation.objects.filter(pk=operation_id).exists() or not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = Operation.objects.get(pk=operation_id)
    calculation = Calculation.objects.get(pk=calculation_id)

    if OperationCalculation.objects.filter(operation=operation, calculation=calculation).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operation_calculation = OperationCalculation.objects.create(operation=operation, calculation=calculation)
    serializer = OperationCalculationSerializer(operation_calculation)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_operation_from_calculation(request, operation_id, calculation_id):
    if not OperationCalculation.objects.filter(operation_id=operation_id, calculation_id=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation_calculation = OperationCalculation.objects.get(operation_id=operation_id, calculation_id=calculation_id)
    operation_calculation.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_operation_in_calculation(request, calculation_id, operation_id):
    try:
        operation_calculation = OperationCalculation.objects.get(calculation_id=calculation_id, operation_id=operation_id)

        if 'value' in request.data:
            operation_calculation.value = request.data['value']

        operation_calculation.save()
        return Response(OperationCalculationSerializer(operation_calculation).data, status=status.HTTP_200_OK)
    except OperationCalculation.DoesNotExist:
        return Response({"error": "OperationCalculation not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def search_operations_in_calculation(request, calculation_id):
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    operations = OperationCalculation.objects.filter(calculation_id=calculation_id)

    data = [
        OperationSerializer(op.operation).data for op in operations
    ]

    return Response({"calculation": CalculationSerializer(calculation).data, "operations": data})
    


# Пользователи
@api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        auth_login(request, user)
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)