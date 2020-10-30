import itertools
from getpass import getpass
from pprint import pprint

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from faker import Faker

from employee.models import User
from inventory.models import Company, Product


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('poll_ids', nargs='+', type=int)
    #
    #     # Named (optional) arguments
    #     parser.add_argument(
    #         '--delete',
    #         action='store_true',
    #         help='Delete poll instead of closing it',
    #     )

    def handle(self, *args, **options):
        faker = Faker()

        print('creating Company:')
        for _ in range(3):
            print(Company.objects.create(name=faker.bs().title()))
        print("Creating Superuser...")
        print(
            f"Superuser created: {User.objects.create_superuser(first_name='SuperUser', username=input('Enter username:'), password=getpass(), company=Company.objects.get(pk=1))}")
        print('creating groups:')
        pprint(Group.objects.bulk_create([
            Group(name='INVENTORY_MANAGER', ),
            Group(name='QUALITY_ASSURANCE', ),
            Group(name='SALES_MANAGER', ),
            Group(name='IT_ADMIN', ),
        ]))

        print('creating User:')
        # for no, (group, company) in enumerate(itertools.product(Group.objects.all(), Company.objects.all()), start=1):
        for no, (company, group,) in enumerate(itertools.product(Company.objects.all(), Group.objects.all()), start=1):
            user = User.objects.create_user(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                username=f'user{no}',
                password='demo123',
                company=company,
            )
            user.groups.add(group)
            print(user)

        print('Fake inventory:')
        for _ in range(100):
            print(Product.objects.create(code=faker.pystr_format(),
                                         name=faker.pystr(max_chars=20),
                                         quantity=faker.pyint(min_value=1, max_value=99),
                                         qa=faker.pybool(),
                                         company=Company.objects.order_by('?').first(),
                                         ))

        print('setting permissions:')
        print('assigning IT_ADMIN -> employee CRUD')
        group = Group.objects.get(name='IT_ADMIN')
        group.permissions.set(Permission.objects.filter(codename__contains='user'))

        print('assigning INVENTORY_MANAGER -> product CRUD')
        group = Group.objects.get(name='INVENTORY_MANAGER')
        group.permissions.set(Permission.objects.filter(codename__contains='product'))

        print('assigning QUALITY_ASSURANCE -> product Update')
        group = Group.objects.get(name='QUALITY_ASSURANCE')
        group.permissions.set([Permission.objects.get(codename='change_product'),
                               Permission.objects.get(codename='view_product')])

        print('assigning SALES_MANAGER -> user Retrieve and product Retrieve')
        group = Group.objects.get(name='SALES_MANAGER')
        group.permissions.set([Permission.objects.get(codename='view_product'),
                               Permission.objects.get(codename='view_user')])

        for role in Group.objects.all():
            print('#' * 80)
            print(f'Users with role: {role}')
            for no, user in enumerate(User.objects.filter(groups=role), start=1):
                print(f'{no}) {user}')
