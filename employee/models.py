from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from inventory.models import Company


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'
