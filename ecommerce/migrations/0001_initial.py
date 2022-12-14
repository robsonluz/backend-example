# Generated by Django 3.2.13 on 2022-10-10 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Ator',
                'verbose_name_plural': 'Atores',
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.CreateModel(
            name='Duvida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.TextField(verbose_name='Pergunta')),
                ('resposta', models.TextField(verbose_name='Resposta')),
            ],
            options={
                'verbose_name': 'Dúvida frequente',
                'verbose_name_plural': 'Dúvidas frequentes',
            },
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('descricao', models.CharField(max_length=100, null=True, verbose_name='Descricao')),
                ('sinopse', models.CharField(max_length=100, verbose_name='Sinopse')),
                ('duracao', models.IntegerField(null=True, verbose_name='Duração')),
                ('fotoCapa', models.ImageField(max_length=255, null=True, upload_to='filmes')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('atores', models.ManyToManyField(to='ecommerce.Ator', verbose_name='Atores')),
            ],
            options={
                'verbose_name': 'Filme',
                'verbose_name_plural': 'Filmes',
            },
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=50, verbose_name='Número')),
                ('capacidade', models.IntegerField(verbose_name='Capacidade')),
            ],
            options={
                'verbose_name': 'Sala',
                'verbose_name_plural': 'Salas',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('email', models.CharField(max_length=100, verbose_name='E-mail')),
                ('telefone', models.CharField(max_length=100, null=True, verbose_name='Telefone')),
                ('cidade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.cidade', verbose_name='Cidade')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário logado')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('filme', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.filme', verbose_name='Filme')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.sala', verbose_name='Sala')),
            ],
            options={
                'verbose_name': 'Sessão',
                'verbose_name_plural': 'Sessões',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlPagamento', models.CharField(max_length=255, null=True, verbose_name='URL Pagamento')),
                ('finalizado', models.BooleanField()),
                ('pago', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.usuario', verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.filme', verbose_name='Filme')),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.pedido', verbose_name='Pedido')),
            ],
        ),
    ]
