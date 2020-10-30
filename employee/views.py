from rest_framework import generics

# Create your views here.
from employee.models import User
from employee.serializers import UserSerializer


class UserListCreate(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if 'SALES_MANAGER' in self.request.user.groups.values_list('name', flat=True):
            return User.objects.filter(groups__name='SALES_MANAGER')
        else:
            return User.objects.all()


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
