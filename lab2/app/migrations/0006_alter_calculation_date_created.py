# Generated by Django 5.1.2 on 2024-10-13 21:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_calculation_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 13, 21, 20, 39, 679155, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]