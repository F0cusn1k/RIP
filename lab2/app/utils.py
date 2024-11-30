import random
from datetime import datetime, timedelta
from django.utils import timezone


def random_date():
    now = datetime.now(tz=timezone.utc)
    return now + timedelta(random.uniform(-1, 0) * 100)


def random_timedelta(factor=100):
    return timedelta(random.uniform(0, 1) * factor)

STATUS_CHOICES = (
        (1, 'Черновик'),
        (2, 'Удалена'),
        (3, 'Сформирована'),
        (4, 'Принята'),
        (5, 'Отклонена')
)