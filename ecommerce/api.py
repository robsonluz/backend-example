from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout


import os

# SDK do Mercado Pago
import mercadopago
# Adicione as credenciais
sdk = mercadopago.SDK(os.environ['mercadopagotoken'])

from ecommerce.models import Cidade
from ecommerce.models import Filme
from ecommerce.models import Ator
from ecommerce.models import Sala
from ecommerce.models import Sessao
from ecommerce.models import Usuario
from ecommerce.models import Item
from ecommerce.models import Pedido

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
    fields = ['id', 'titulo', 'descricao', 'sinopse', 'atores', 'fotoCapa', 'valor']

class FilmeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Filme.objects.all().order_by('titulo')
  serializer_class = FilmeSerializer 
  def get_queryset(self):
    """
    Filtra filme por titulo e ator
    """
    queryset = Filme.objects.all().order_by('titulo')
    query = {}

    titulo = self.request.query_params.get('titulo', None)
    if titulo is not None:
      query['titulo'] = titulo


    ator = self.request.query_params.get('ator', None)  
    if ator is not None:
      query['atores'] = ator

    print(query)
    queryset = queryset.filter(**query)    
    return queryset  
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







#### API de autenticação ###############################
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'cidade', 'user']

class CreateUsuarioSerializer(serializers.ModelSerializer):
    cidade: CidadeSerializer()
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'cidade', 'user']

class CreateUsuarioViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateUsuarioSerializer   
  queryset = Usuario.objects.all()
  def perform_create(self, serializer):
    serializer.save(user = self.request.user)   

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
        ]
    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
  serializer_class = UserRegistrationSerializer  

class LoginViewSet(ViewSet):
  @staticmethod
  def create(request: Request) -> Response:
      user = authenticate(
          username=request.data.get('username'),
          password=request.data.get('password'))

      if user is not None:
        login(request, user)
        return JsonResponse({"id": user.id, "username": user.username})
      else:
        return JsonResponse(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

class UsuarioDetailsViewSet(ViewSet):
  serializer_class = UsuarioSerializer
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    usuarios = Usuario.objects.filter(user = request.user)
    usuario = usuarios[0] if usuarios.exists() else None
    serializer = UsuarioSerializer(usuario, many=False)
    return Response(serializer.data)

class UserDetailsSerializer(serializers.ModelSerializer):
  class Meta:
      model = get_user_model()
      fields = ('id', 'username')

class UserDetailsViewSet(ViewSet):
  serializer_class = UserDetailsSerializer
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    serializer = UserDetailsSerializer(request.user, many=False)
    return Response(serializer.data)


class LogoutViewSet(ViewSet):
  permission_classes = [IsAuthenticated]
  @staticmethod
  def list(request: Request) -> Response:
    logout(request)
    content = {'logout': 1}
    return Response(content)  
######################################################        
  







############ Pedidos, Carrinho de compras ###########
class ItemSerializer(serializers.ModelSerializer):
    filme: FilmeSerializer()
    class Meta:
        model = Item
        depth = 2
        fields = ['id', 'valor', 'filme']

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemSerializer(many=True)
    class Meta:
        model = Pedido
        depth = 2
        fields = ['id', 'finalizado', 'valorTotal', 'itens', 'urlPagamento','pago']

class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer      
    def get_queryset(self):
      #filtra apenas os pedidos do usuário logado
      return Pedido.objects.filter(usuario = Usuario.objects.filter(user = self.request.user)[0], finalizado = True)    

class CarrinhoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer      
    def get_queryset(self):
      #filtra apenas os pedidos do usuário logado
      return Pedido.objects.filter(usuario = Usuario.objects.filter(user = self.request.user)[0], finalizado = False)          

class CreateItemSerializer(serializers.ModelSerializer):
    filme: FilmeSerializer()
    class Meta:
        model = Item
        fields = ['id', 'filme', 'pedido']

class CreateItemPedidoViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
  serializer_class = CreateItemSerializer   
  queryset = Item.objects.all()

  def perform_create(self, serializer):
    #procura o pedido aberto
    pedidosAbertos = Pedido.objects.filter(finalizado = False, usuario = Usuario.objects.filter(user = self.request.user)[0])    
    if(len(pedidosAbertos) > 0):
      pedidoAberto = pedidosAbertos[0]
    else:
      #caso nao exista um pedido aberto ele cria um
      pedidoAberto = Pedido.objects.create(usuario = Usuario.objects.filter(user = self.request.user)[0], finalizado = False)
    serializer.save(pedido = pedidoAberto) 



class FinalizarPedidoViewSet(ViewSet):
  @staticmethod
  def create(request: Request) -> Response:
      print("chegou aqui no finalizar")
      id = request.data.get('id')
      print(id)
      pedidos = Pedido.objects.filter(id = id)
      if(len(pedidos) > 0):
        pedido = pedidos[0]

        items = []
        for item in pedido.itens:
          items.append({
            "title": item.filme.titulo,
            "quantity": 1,
            "unit_price": float(item.valor)
          })

        url="https://testedjango.robsonjoo.repl.co/api/pagamento/?pedido=" + str(request.data.get('id'))

        # Cria um item na preferência
        preference_data = {
          "items": items,
          "external_reference": str(id),
          "notification_url": url,
        }

        print(preference_data)
    
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        print(preference)
        print(preference['sandbox_init_point'])
        pedido.urlPagamento = str(preference['sandbox_init_point'])
        pedido.finalizado = True
        Pedido.save(pedido)   
        return JsonResponse({"id": pedido.id, "urlPagamento": pedido.urlPagamento})
      return JsonResponse({})



class PagamentoViewSet(ViewSet):
  @staticmethod
  def create(request: Request) -> Response:
      pedidoId = request.query_params.get('pedido', None)
      if pedidoId is not None:
        pedidos = Pedido.objects.filter(id = pedidoId)
        if(len(pedidos) > 0):
          pedido = pedidos[0]
          pedido.pago = True
          Pedido.save(pedido)
          
      return JsonResponse({})    
    
####################################################################   







# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cidades', CidadeViewSet)
router.register(r'filmes', FilmeViewSet)
router.register(r'atores', AtorViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'sessoes', SessaoViewSet)


#Rotas de autenticação
router.register(r'currentuser', UserDetailsViewSet, basename="Currentuser")
router.register(r'currentusuario', UsuarioDetailsViewSet, basename="Currentusuario")
router.register(r'login', LoginViewSet, basename="Login")
router.register(r'logout', LogoutViewSet, basename="Logout")
router.register(r'user-registration', UserRegistrationViewSet, basename="User")
router.register(r'usuarios-create', CreateUsuarioViewSet)


# Rotas do pedido
router.register(r'pedidos', PedidoViewSet, basename='Pedidos')
router.register(r'carrinho', CarrinhoViewSet, basename='Carrinho')
router.register(r'item-pedido-create', CreateItemPedidoViewSet)
router.register(r'pedido-finalizar', FinalizarPedidoViewSet, basename='PedidoFinalizar')
router.register(r'pagamento', PagamentoViewSet, basename='Pagamento')