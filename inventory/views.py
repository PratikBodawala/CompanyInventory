from rest_framework import generics
# Create your views here.
from rest_framework.response import Response

from inventory.models import Company, Product
from inventory.serializers import CompanySerializer, ProductSerializer


class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if 'QUALITY_ASSURANCE' in self.request.user.groups.values_list('name', flat=True) \
                or self.request.user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.filter(company=self.request.user.company)


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'QUALITY_ASSURANCE' in request.user.groups.values_list('name', flat=True):
            partial = True
            data = {'qa': request.data.get('qa', False)}
            serializer = self.get_serializer(instance, data=data, partial=partial)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
