from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from ecommerce.models import Cidade

# Serializers define the API representation.
class CidadeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cidade
    fields = ['id', 'nome']

# ViewSets define the view behavior.
class CidadeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Cidade.objects.all().order_by('nome')
  serializer_class = CidadeSerializer 


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cidades', CidadeViewSet)
