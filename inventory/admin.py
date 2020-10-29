from django.contrib import admin

# Register your models here.
from inventory.models import Product, Company

admin.site.register(Company)
admin.site.register(Product)
