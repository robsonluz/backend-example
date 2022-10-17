from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from ecommerce.models import Cidade
from ecommerce.models import Filme
from ecommerce.models import Ator
from ecommerce.models import Sala
from ecommerce.models import Sessao

#### Cidades ########################################
class CidadeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cidade
    fields = ['id', 'nome']

class CidadeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Cidade.objects.all().order_by('nome')
  serializer_class = CidadeSerializer 
######################################################

#### Atores ########################################
class AtorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ator
    fields = ['id', 'nome']
    
class AtorViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Ator.objects.all().order_by('nome')
  serializer_class = AtorSerializer
######################################################    

#### Filmes ########################################
class FilmeSerializer(serializers.ModelSerializer):
  atores = AtorSerializer(many=True, read_only=True)  
  class Meta:
    model = Filme
    fields = ['id', 'titulo', 'descricao', 'sinopse', 'atores']

class FilmeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Filme.objects.all().order_by('titulo')
  serializer_class = FilmeSerializer 
######################################################

#### Sala ########################################
class SalaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sala
    fields = ['id', 'numero', 'capacidade']

class SalaViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Sala.objects.all().order_by('numero')
  serializer_class = SalaSerializer
######################################################  

#### Sessão ########################################
class SessaoSerializer(serializers.ModelSerializer):
  filme = FilmeSerializer()  
  sala = SalaSerializer()  
  class Meta:
    model = Sessao
    fields = ['id', 'data', 'sala', 'filme']

class SessaoViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Sessao.objects.all().order_by('data')
  serializer_class = SessaoSerializer 
######################################################  
  


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cidades', CidadeViewSet)
router.register(r'filmes', FilmeViewSet)
router.register(r'atores', AtorViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'sessoes', SessaoViewSet)

