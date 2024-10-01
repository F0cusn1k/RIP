import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234")
    User.objects.create_superuser("root", "root@root.com", "1234")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234")

    print("Пользователи созданы")


def add_operations():
    Operation.objects.create(
        name="Факторил",
        description="Факториал — это произведение всех натуральных чисел от 1 до данного числа. Например, факториал числа 5 будет равен 1 × 2 × 3 × 4 × 5 = 120. Его используют во многих областях науки — например, комбинаторике, теории вероятностей и математическом анализе.",
        parameters=1,
        image="images/1.png"
    )

    Operation.objects.create(
        name="Корень",
        description="Арифметическим квадратным корнем из числа называется неотрицательное число, квадрат которого равен данному числу.",
        parameters=1,
        image="images/2.png"
    )

    Operation.objects.create(
        name="Логарифм",
        description="Логарифмом числа b по основанию a называют показатель степени с основанием a, равной b. То есть, попросту говоря, логарифм — это степень, в которую нужно возвести a для получения b.",
        parameters=2,
        image="images/3.png"
    )

    Operation.objects.create(
        name="НОК",
        description="Наименьшее общее кратное для нескольких чисел — это наименьшее натуральное число, которое делится на каждое из этих чисел..",
        parameters=2,
        image="images/4.png"
    )

    Operation.objects.create(
        name="НОД",
        description="Наибольший общий делитель (НОД) двух чисел – это наибольшее число, на которое каждое из этих чисел можно поделить без остатка.",
        parameters=2,
        image="images/5.png"
    )

    Operation.objects.create(
        name="Сочетание",
        description="Сочетание — это неупорядоченный набор элементов, взятых из множества. В сочетании используется только выбор, расположение не используется.",
        parameters=2,
        image="images/6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_calculations():
    users = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    operations = Operation.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        add_calculation(status, operations, users, moderators)

    add_calculation(1, operations, users, moderators)

    print("Заявки добавлены")


def add_calculation(status, operations, users, moderators):
    calculation = Calculation.objects.create()
    calculation.status = status

    if calculation.status in [3, 4]:
        calculation.date_complete = random_date()
        calculation.date_formation = calculation.date_complete - random_timedelta()
        calculation.date_created = calculation.date_formation - random_timedelta()
    else:
        calculation.date_formation = random_date()
        calculation.date_created = calculation.date_formation - random_timedelta()

    calculation.owner = random.choice(users)
    calculation.moderator = random.choice(moderators)

    calculation.number = random.randint(1, 10)

    for operation in random.sample(list(operations), 3):
        item = OperationCalculation(
            calculation=calculation,
            operation=operation,
            value=random.randint(1, 10)
        )
        item.save()

    calculation.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_operations()
        add_calculations()



















