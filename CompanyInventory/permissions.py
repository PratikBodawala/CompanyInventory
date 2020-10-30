import copy

from rest_framework import permissions

from employee.models import User
from inventory.models import Product


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class CustomDjangoObjectPermissions(permissions.DjangoObjectPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def has_object_permission(self, request, view, obj):
        req_groups = request.user.groups.values_list('name', flat=True)
        if 'INVENTORY_MANAGER' in req_groups and isinstance(obj, Product):
            return obj.company == request.user.company
        if 'QUALITY_ASSURANCE' in req_groups and isinstance(obj, Product):
            return True
        if 'SALES_MANAGER' in req_groups and isinstance(obj, User):
            return 'SALES_MANAGER' in obj.groups.values_list('name', flat=True)
        if 'SALES_MANAGER' in req_groups and isinstance(obj, Product):
            return obj.company == request.user.company
        return False
