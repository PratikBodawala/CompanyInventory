from django.urls import path

from employee import views

urlpatterns = [
    path('employee/', views.UserListCreate.as_view(), name='user-lc'),
    path('employee/<pk>', views.UserRetrieveUpdateDestroy.as_view(), name='user-rud'),
]
