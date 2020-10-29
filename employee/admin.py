from django.contrib import admin

# Register your models here.
from employee.models import User

admin.site.register(User)
