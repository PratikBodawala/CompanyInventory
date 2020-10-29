from django.db import models
from employee.models import User


class Company(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    quantity = models.IntegerField()
    qa = models.BooleanField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.code = self.code.upper()
        self.save_base(True)

    def __str__(self):
        return f'{self.name}({self.code})'
