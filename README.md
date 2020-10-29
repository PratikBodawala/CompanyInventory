# Company Inventory

### Get started

python version 3.8
```bash
virtualenv -p python3.8 venv
./manage.py migrate
./manage.py initialsetup
```

## Models

- Users
- Company
- Product

## Roles

- INVENTORY_MANAGER
- QUALITY_ASSURANCE
- SALES_MANAGER
- IT_ADMIN

## routes

- /api/company
- /api/company/{pk}
- /api/product
- /api/product/{pk}