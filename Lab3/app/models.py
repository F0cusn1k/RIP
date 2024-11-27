# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin, User
# from django.db import models


# class Astronaut(models.Model):
#     STATUS_CHOICES = (
#         (1, 'Действует'),
#         (2, 'Удалена'),
#     )

#     name = models.CharField(max_length=100, verbose_name="Название")
#     description = models.TextField(max_length=500, verbose_name="Описание",)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
#     image = models.ImageField(verbose_name="Фото", blank=True, null=True)

#     space_time = models.IntegerField(blank=True)
#     specialization = models.CharField(blank=True)
#     country = models.CharField(blank=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Астронавт"
#         verbose_name_plural = "Астронавты"
#         db_table = "astronauts"


# class Flight(models.Model):
#     STATUS_CHOICES = (
#         (1, 'Введён'),
#         (2, 'В работе'),
#         (3, 'Завершен'),
#         (4, 'Отклонен'),
#         (5, 'Удален')
#     )

#     status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
#     date_created = models.DateTimeField(verbose_name="Дата создания", blank=True, null=True)
#     date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
#     date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

#     owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
#     moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', blank=True,  null=True)

#     name = models.CharField(verbose_name="Название", blank=True, null=True)
#     description = models.TextField(verbose_name="Биография", blank=True, null=True)
#     date = models.DateField(verbose_name="Дата", blank=True, null=True)

#     def __str__(self):
#         return "Полет №" + str(self.pk)

#     class Meta:
#         verbose_name = "Полет"
#         verbose_name_plural = "Полеты"
#         db_table = "flights"
#         ordering = ('-date_formation', )


# class AstronautFlight(models.Model):
#     astronaut = models.ForeignKey(Astronaut, on_delete=models.DO_NOTHING, blank=True, null=True)
#     flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING, blank=True, null=True)
#     value = models.BooleanField(verbose_name="Поле м-м", default=0)

#     def __str__(self):
#         return "м-м №" + str(self.pk)

#     class Meta:
#         verbose_name = "м-м"
#         verbose_name_plural = "м-м"
#         db_table = "astronaut_flight"
#         constraints = [
#             models.UniqueConstraint(fields=['astronaut', 'flight'], name="astronaut_flight_constraint")
#         ]

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User


class Operation(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название", blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="images/default.png", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    parameters = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        db_table = "operations"


class Calculation(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    number = models.IntegerField(blank=True, null=True)
    calculation_creator = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Вычисление №" + str(self.pk)

    def get_operations(self):
        return [
            setattr(item.operation, "value", item.value) or item.operation
            for item in OperationCalculation.objects.filter(calculation=self)
        ]

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Вычисление"
        verbose_name_plural = "Вычисления"
        ordering = ('-date_formation', )
        db_table = "calculations"


class OperationCalculation(models.Model):
    operation = models.ForeignKey(Operation, models.DO_NOTHING, blank=True, null=True)
    calculation = models.ForeignKey(Calculation, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "operation_calculation"