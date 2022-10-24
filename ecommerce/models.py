from django.db import models
from django.contrib.auth import get_user_model
from functools import reduce

User = get_user_model()

class Ator(models.Model):
  nome = models.CharField("Nome", max_length=100)
  def __str__(self):
      return self.nome
  class Meta:
      verbose_name = "Ator"
      verbose_name_plural = "Atores"


class Filme(models.Model):
  titulo = models.CharField("Título", max_length=100)
  descricao = models.CharField("Descricao", max_length=100, null=True)
  sinopse = models.CharField("Sinopse", max_length=100)
  duracao = models.IntegerField("Duração", null=True)
  atores = models.ManyToManyField("Ator", verbose_name="Atores")
  fotoCapa = models.ImageField(upload_to='filmes', max_length=255, null=True)
  valor = models.DecimalField(max_digits=5, decimal_places=2, null=True)
  
  def __str__(self):
      return self.titulo
  class Meta:
      verbose_name = "Filme"
      verbose_name_plural = "Filmes"


class Sessao(models.Model):
  data = models.DateTimeField("Data")
  sala = models.ForeignKey('Sala', on_delete=models.PROTECT, verbose_name="Sala")
  filme = models.ForeignKey('Filme', on_delete=models.PROTECT, verbose_name="Filme")
  def __str__(self):
      return f"{self.data} - {self.filme} - sala: {self.sala}"
  class Meta:
      verbose_name = "Sessão"
      verbose_name_plural = "Sessões"


class Sala(models.Model):
  numero = models.CharField("Número", max_length=50)
  capacidade = models.IntegerField("Capacidade")
  def __str__(self):
      return str(self.numero)
  class Meta:
      verbose_name = "Sala"
      verbose_name_plural = "Salas"
    
  @property
  def sessoes(self):
    return Sessao.objects.filter(sala=self)    


class Duvida(models.Model):
  pergunta = models.TextField("Pergunta")
  resposta = models.TextField("Resposta")
  def __str__(self):
      return str(self.pergunta)
  class Meta:
      verbose_name = "Dúvida frequente"
      verbose_name_plural = "Dúvidas frequentes"

class Cidade(models.Model):
  nome = models.CharField("Nome", max_length=255)
  
  def __str__(self):
      return self.nome
  class Meta:
      verbose_name = "Cidade"
      verbose_name_plural = "Cidades"  

class Usuario(models.Model):
  nome = models.CharField("Nome", max_length=255)
  email = models.CharField("E-mail", max_length=100)
  telefone = models.CharField("Telefone", max_length=100, null=True)
  cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT, verbose_name="Cidade", null=True)
  user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário logado", null=True)

  def __str__(self):
      return self.nome
  class Meta:
      verbose_name = "Usuário"
      verbose_name_plural = "Usuários"    

class Pedido(models.Model):
  usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name="Usuário", null=True)
  urlPagamento = models.CharField("URL Pagamento", max_length=255, null=True)
  finalizado = models.BooleanField()
  pago = models.BooleanField(default=False)

  @property
  def itens(self):
    return Item.objects.filter(pedido=self)

  @property
  def valorTotal(self):
    #busca os itens deste pedido
    itens = list(Item.objects.filter(pedido=self))

    #soma os valores dos itens no pedido
    return reduce(lambda x, y: x + y, list(map(lambda item: item.valor, itens)), 0)

class Item(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, verbose_name="Pedido", null=True)
  filme = models.ForeignKey(Filme, on_delete=models.PROTECT, verbose_name="Filme", null=True)

  @property
  def valor(self):
    return self.filme.valor