# from django.contrib.auth import authenticate
# from django.utils import timezone
# from django.utils.dateparse import parse_datetime
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .management.commands.fill_db import calc
# from .serializers import *


# def get_draft_flight():
#     return Flight.objects.filter(status=1).first()


# def get_user():
#     return User.objects.filter(is_superuser=False).first()


# def get_moderator():
#     return User.objects.filter(is_superuser=True).first()


# @api_view(["GET"])
# def search_astronauts(request):
#     astronaut_name = request.GET.get("astronaut_name", "")

#     astronauts = Astronaut.objects.filter(status=1)

#     if astronaut_name:
#         astronauts = astronauts.filter(name__icontains=astronaut_name)

#     serializer = AstronautsSerializer(astronauts, many=True)
    
#     draft_flight = get_draft_flight()

#     resp = {
#         "astronauts": serializer.data,
#         "astronauts_count": AstronautFlight.objects.filter(flight=draft_flight).count() if draft_flight else None,
#         "draft_flight": draft_flight.pk if draft_flight else None
#     }

#     return Response(resp)


# @api_view(["GET"])
# def get_astronaut_by_id(request, astronaut_id):
#     if not Astronaut.objects.filter(pk=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     astronaut = Astronaut.objects.get(pk=astronaut_id)
#     serializer = AstronautSerializer(astronaut)

#     return Response(serializer.data)


# @api_view(["PUT"])
# def update_astronaut(request, astronaut_id):
#     if not Astronaut.objects.filter(pk=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     astronaut = Astronaut.objects.get(pk=astronaut_id)

#     serializer = AstronautSerializer(astronaut, data=request.data, partial=True)

#     if serializer.is_valid(raise_exception=True):
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["POST"])
# def create_astronaut(request):
#     serializer = AstronautSerializer(data=request.data, partial=False)

#     serializer.is_valid(raise_exception=True)

#     Astronaut.objects.create(**serializer.validated_data)

#     astronauts = Astronaut.objects.filter(status=1)
#     serializer = AstronautSerializer(astronauts, many=True)

#     return Response(serializer.data)


# @api_view(["DELETE"])
# def delete_astronaut(request, astronaut_id):
#     if not Astronaut.objects.filter(pk=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     astronaut = Astronaut.objects.get(pk=astronaut_id)
#     astronaut.status = 2
#     astronaut.save()

#     astronauts = Astronaut.objects.filter(status=1)
#     serializer = AstronautSerializer(astronauts, many=True)

#     return Response(serializer.data)


# @api_view(["POST"])
# def add_astronaut_to_flight(request, astronaut_id):
#     if not Astronaut.objects.filter(pk=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     astronaut = Astronaut.objects.get(pk=astronaut_id)

#     draft_flight = get_draft_flight()

#     if draft_flight is None:
#         draft_flight = Flight.objects.create()
#         draft_flight.owner = get_user()
#         draft_flight.date_created = timezone.now()
#         draft_flight.save()

#     if AstronautFlight.objects.filter(flight=draft_flight, astronaut=astronaut).exists():
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
#     item = AstronautFlight.objects.create()
#     item.flight = draft_flight
#     item.astronaut = astronaut
#     item.save()

#     serializer = FlightSerializer(draft_flight)
#     return Response(serializer.data["astronauts"])


# @api_view(["POST"])
# def update_astronaut_image(request, astronaut_id):
#     if not Astronaut.objects.filter(pk=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     astronaut = Astronaut.objects.get(pk=astronaut_id)

#     image = request.data.get("image")
#     if image is not None:
#         astronaut.image = image
#         astronaut.save()

#     serializer = AstronautSerializer(astronaut)

#     return Response(serializer.data)


# @api_view(["GET"])
# def search_flights(request):
#     status = int(request.GET.get("status", 0))
#     date_formation_start = request.GET.get("date_formation_start")
#     date_formation_end = request.GET.get("date_formation_end")

#     flights = Flight.objects.exclude(status__in=[1, 5])

#     if status > 0:
#         flights = flights.filter(status=status)

#     if date_formation_start and parse_datetime(date_formation_start):
#         flights = flights.filter(date_formation__gte=parse_datetime(date_formation_start))

#     if date_formation_end and parse_datetime(date_formation_end):
#         flights = flights.filter(date_formation__lt=parse_datetime(date_formation_end))

#     serializer = FlightsSerializer(flights, many=True)

#     return Response(serializer.data)


# @api_view(["GET"])
# def get_flight_by_id(request, flight_id):
#     if not Flight.objects.filter(pk=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     flight = Flight.objects.get(pk=flight_id)
#     serializer = FlightSerializer(flight, many=False)

#     return Response(serializer.data)


# @api_view(["PUT"])
# def update_flight(request, flight_id):
#     if not Flight.objects.filter(pk=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     flight = Flight.objects.get(pk=flight_id)
#     serializer = FlightSerializer(flight, data=request.data, partial=True)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["PUT"])
# def update_status_user(request, flight_id):
#     if not Flight.objects.filter(pk=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     flight = Flight.objects.get(pk=flight_id)

#     if flight.status != 1:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     flight.status = 2
#     flight.date_formation = timezone.now()
#     flight.save()

#     serializer = FlightSerializer(flight, many=False)

#     return Response(serializer.data)


# @api_view(["PUT"])
# def update_status_admin(request, flight_id):
#     if not Flight.objects.filter(pk=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     request_status = int(request.data["status"])

#     if request_status not in [3, 4]:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     flight = Flight.objects.get(pk=flight_id)

#     if flight.status != 2:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     if request_status == 3:
#         flight.date = calc()

#     flight.date_complete = timezone.now()
#     flight.status = request_status
#     flight.moderator = get_moderator()
#     flight.save()

#     return Response(status=status.HTTP_200_OK)


# @api_view(["DELETE"])
# def delete_flight(request, flight_id):
#     if not Flight.objects.filter(pk=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     flight = Flight.objects.get(pk=flight_id)

#     if flight.status != 1:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     flight.status = 5
#     flight.save()

#     serializer = FlightSerializer(flight, many=False)

#     return Response(serializer.data)


# @api_view(["DELETE"])
# def delete_astronaut_from_flight(request, flight_id, astronaut_id):
#     if not AstronautFlight.objects.filter(flight_id=flight_id, astronaut_id=astronaut_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     item = AstronautFlight.objects.get(flight_id=flight_id, astronaut_id=astronaut_id)
#     item.delete()

#     items = AstronautFlight.objects.filter(flight_id=flight_id)
#     data = [AstronautItemSerializer(item.astronaut, context={"value": item.value}).data for item in items]

#     return Response(data, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def update_astronaut_in_flight(request, flight_id, astronaut_id):
#     if not AstronautFlight.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     item = AstronautFlight.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)

#     serializer = AstronautFlightSerializer(item, data=request.data,  partial=True)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["POST"])
# def register(request):
#     serializer = UserRegisterSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(status=status.HTTP_409_CONFLICT)

#     user = serializer.save()

#     serializer = UserSerializer(user)

#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["POST"])
# def login(request):
#     serializer = UserLoginSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

#     user = authenticate(**serializer.data)
#     if user is None:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

#     serializer = UserSerializer(user)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def logout(request):
#     return Response(status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def update_user(request, user_id):
#     if not User.objects.filter(pk=user_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     user = User.objects.get(pk=user_id)
#     serializer = UserSerializer(user, data=request.data, partial=True)

#     if not serializer.is_valid():
#         return Response(status=status.HTTP_409_CONFLICT)

#     serializer.save()

#     return Response(serializer.data)

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt


@api_view(["GET"])
def search_operations(request):
    operation_name = request.GET.get("operation_name", "")

    operations = Operation.objects.all()

    if operation_name:
        operations = operations.filter(name__icontains=operation_name)

    serializer = OperationSerializer(operations, many=True)
    return Response(serializer.data)


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


@api_view(["DELETE"])
def delete_operation(request, operation_id):
    if not Operation.objects.filter(pk=operation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = Operation.objects.get(pk=operation_id)
    operation.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def search_calculations(request):
    calculation_name = request.GET.get("calculation_name", "")

    calculations = Calculation.objects.all()

    if calculation_name:
        calculations = calculations.filter(name__icontains=calculation_name)

    serializer = CalculationSerializer(calculations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_calculation_by_id(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)
    serializer = CalculationSerializer(calculation)
    return Response(serializer.data)


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


@api_view(["DELETE"])
def delete_calculation(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)
    calculation.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


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
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operations = OperationCalculation.objects.filter(calculation_id=calculation_id)
    data = [OperationSerializer(op.operation).data for op in operations]

    return Response(data)
    


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




# from django.contrib.auth.models import User
# from django.db import connection
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone

# from app.models import Operation, Calculation, OperationCalculation

# from math import factorial, gcd


# def index(request):
#     operation_name = request.GET.get("operation_name", "")
#     operations = Operation.objects.filter(status=1)

#     if operation_name:
#         operations = operations.filter(name__icontains=operation_name)

#     draft_calculation = get_draft_calculation()

#     context = {
#         "operation_name": operation_name,
#         "operations": operations
#     }
#     for operation in operations:
#          operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

#     if draft_calculation:
#         context["operations_count"] = len(draft_calculation.get_operations())
#         context["draft_calculation"] = draft_calculation

#     return render(request, "operations_page.html", context)


# def add_operation_to_draft_calculation(request, operation_id):
#     operation = Operation.objects.get(pk=operation_id)

#     draft_calculation = get_draft_calculation()

#     if draft_calculation is None:
#         draft_calculation = Calculation.objects.create()
#         draft_calculation.owner = get_current_user()
#         draft_calculation.date_created = timezone.now()
#         draft_calculation.save()


#     if OperationCalculation.objects.filter(calculation=draft_calculation, operation=operation).exists():
#         return redirect("/")

#     item = OperationCalculation(
#         calculation=draft_calculation,
#         operation=operation
#     )
#     item.save()

#     return redirect("/")


# def operation_details(request, operation_id):

#     operation = Operation.objects.get(id=operation_id)
#     operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"
    
#     context = {
#         "operation": operation
#     }

#     return render(request, "operation_page.html", context)

# def calculation(request, calculation_id):
#     calculation = get_object_or_404(Calculation, pk=calculation_id)
#     calculation_number = request.GET.get("calculation_number", "")
#     calculation_creator = request.GET.get("calculation_creator", "")
#     if calculation.status == 5:
#         return redirect("/")

#     operations = calculation.get_operations()
#     for operation in operations:
#         operation.image_url = f"http://127.0.0.1:9000/rip/{operation.image}"

#     context = {
#         "calculation": calculation,
#         "operations": operations,
#         "calculation_number": calculation_number,
#         "calculation_creator": calculation_creator,
#     }
#     return render(request, "calculation_page.html", context)

# def delete_calculation(request, calculation_id):
#     if request.method == 'POST':
#         calculation = get_object_or_404(Calculation, pk=calculation_id)
#         new_calculation_number = request.POST.get('calculation_number', '').strip()
#         new_calculation_creator = request.POST.get('calculation_creator', '').strip()
        
#         if not new_calculation_number.isdigit():
#             return render(request, 'error_page.html', {'error': 'Не введено корректное число для обработки'})
        
#         new_calculation_number = int(new_calculation_number)

#         # Обновление поля `value` для связанных записей OperationCalculation
#         related_operations = OperationCalculation.objects.filter(calculation_id=calculation_id)

#         for op_calc in related_operations:
#             if op_calc.operation and op_calc.operation.id == 1:
#                 op_calc.value = factorial(new_calculation_number)
#             elif op_calc.operation:
#                 op_calc.value = gcd(op_calc.operation.id, new_calculation_number)
#             else:
#                 op_calc.value = None  # Если `operation` отсутствует, оставляем значение пустым
#             op_calc.save()

#         # Обновление записи Calculation
#         calculation.calculation_creator = new_calculation_creator
#         calculation.number = new_calculation_number
#         calculation.status = 5
#         calculation.save()

#         return redirect("/")
#     else:
#         return redirect("/")

# def get_draft_calculation():
#     return Calculation.objects.filter(status=1).first()


# def get_current_user():
#     return User.objects.filter(is_superuser=False).first()