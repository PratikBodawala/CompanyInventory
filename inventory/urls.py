from django.urls import path

from inventory import views

urlpatterns = [
    path('company/', views.CompanyListCreate.as_view(), name='company-lc'),
    path('company/<pk>', views.CompanyRetrieveUpdateDestroy.as_view(), name='company-rud'),
    path('product/', views.ProductListCreate.as_view(), name='product-lc'),
    path('product/<pk>', views.ProductRetrieveUpdateDestroy.as_view(), name='product-rud'),
]
