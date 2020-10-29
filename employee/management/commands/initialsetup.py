from pprint import pprint
from random import randint

from django.contrib.auth.models import Group
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
        print(
            f"Superuser created: {User.objects.create_superuser(first_name='Pratik', username='pratik', password='superuser')}")
        print('creating groups:')
        pprint(Group.objects.bulk_create([
            Group(name='INVENTORY_MANAGER', ),
            Group(name='QUALITY_ASSURANCE', ),
            Group(name='SALES_MANAGER', ),
            Group(name='IT_ADMIN', ),
        ]))
        print('creating User:')
        for no in range(1, 21):
            print(User.objects.create_user(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                username=f'user{no}',
                password='demo123', ))
        print('creating Company:')
        for _ in range(8):
            print(Company.objects.create(name=faker.bs().title(), user=User.objects.get(pk=randint(2, 21)), ))
        print('Fake inventory:')
        for _ in range(100):
            print(Product.objects.create(code=faker.pystr_format(),
                                         name=faker.pystr(max_chars=20),
                                         quantity=faker.pyint(min_value=1, max_value=99),
                                         qa=faker.pybool(),
                                         company=Company.objects.order_by('?').first(),
                                         ))
