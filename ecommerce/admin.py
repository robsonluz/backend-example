from django.contrib import admin

# Register your models here.
from .models import Ator
from .models import Filme
from .models import Sessao
from .models import Sala
from .models import Duvida
from .models import Usuario
from .models import Cidade
from .models import Pedido
from .models import Item

admin.site.register(Ator)
admin.site.register(Filme)
admin.site.register(Sessao)
admin.site.register(Sala)
admin.site.register(Duvida)
admin.site.register(Usuario)
admin.site.register(Cidade)
admin.site.register(Pedido)
admin.site.register(Item)
