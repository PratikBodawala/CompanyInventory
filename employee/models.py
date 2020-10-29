from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name()


