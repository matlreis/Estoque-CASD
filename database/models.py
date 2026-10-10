from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AdminManager(BaseUserManager):
    def create_user(self, email, nome_user, nome, password=None):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome_user=nome_user, nome=nome)
        
        # O set_password absorve a necessidade das suas colunas SALT e HASH
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_user, nome, password=None):
        user = self.create_user(email, nome_user, nome, password)
        user.is_superuser = True
        user.is_staff = True  # Permite acesso ao painel de controle nativo
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser, PermissionsMixin):
    # Campos baseados no seu diagrama ER
    nome = models.CharField(max_length=255)
    nome_user = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    # O Django gerencia os timestamps automaticamente com estas flags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # O Django requer que o campo ACTIVE se chame is_active internamente
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminManager()

    # Define o que será usado para fazer login (pode trocar para 'nome_user' se preferir)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_user', 'nome']

    class Meta:
        db_table = 'admin' # Força o nome da tabela no PostgreSQL para bater com o seu diagrama

    def __str__(self):
        return self.nome_user

class Log_admin(models.Model):
    id_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='ID_ADMIN')

    ip_aparelho = models.CharField(max_length=15, validators=[MinLengthValidator(15)])
    
    event_data = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20)

class Item(models.Model):
    class TipoEstoque(models.TextChoices):
        CASD = 'CASD'
        ZELA = 'ZELADORIA'

    nome = models.CharField(max_length=255)

    tipo_estoque = models.CharField(max_length=20, choices=TipoEstoque.choices)

    quant_total = models.PositiveBigIntegerField()
    quant_uso = models.PositiveBigIntegerField()

class Uso(models.Model):
    id_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    id_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='ID_ADMIN')
    
    is_active = models.BooleanField(default=True)

    limit_data = models.DateTimeField()

class Log_uso(models.Model):
    id_uso = models.ForeignKey(Uso, on_delete=models.CASCADE)

    ip_aparelho = models.CharField(max_length=15, validators=[MinLengthValidator(15)])
    
    event_data = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20)

class Morador(models.Model):
    nome = models.CharField(max_length=255)
    ap = models.CharField(max_length=4)

class Emprestimo(models.Model):
    id_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    id_morador = models.ForeignKey(Morador, on_delete=models.PROTECT)
    
    is_active = models.BooleanField(default=True)

    limit_data = models.DateTimeField()

class Log_Emprestimo(models.Model):
    id_empresitmo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)

    ip_aparelho = models.CharField(max_length=15, validators=[MinLengthValidator(15)])
    
    event_data = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20)