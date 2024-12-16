from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Estado(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.nome} - {self.estado.sigla}' 

class Endereco(models.Model):
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return f'{self.cidade.nome} - {self.cidade.estado.sigla}'

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True, blank=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Profissional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE, default=None, null=True, blank=True)
    CRM = models.IntegerField(unique=True, default=None)
    biografia = models.TextField(blank=True, null=True)
    preco_servico = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_nota_media(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return avaliacoes.aggregate(models.Avg('nota'))['nota__avg']
        return None
    
    def __str__(self):
        if self.especialidade:
            return f'{self.usuario.username} - {self.especialidade.nome}'
        return self.usuario.username


class Servico(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='servicos')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicos_contratados')
    data_agendamento = models.DateTimeField()
    data_realizacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado')
    ], default='AGENDADO')

    def __str__(self):
        return f'Profissional: {self.profissional.usuario.username} ({self.profissional.especialidade.nome}) - Cliente: {self.cliente.username}'

class Avaliacao(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='avaliacoes')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servico = models.OneToOneField(Servico, on_delete=models.CASCADE)
    nota = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profissional: {self.profissional.usuario.username} ({self.profissional.especialidade.nome}) - Cliente: {self.cliente.username} - Nota: {self.nota}'
