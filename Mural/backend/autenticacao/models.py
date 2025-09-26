from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_unb_email(value):
    # Expressão regular para verificar o formato do email UnB
    if not re.match(r'^\d{9}@aluno\.unb\.br$', value):
        raise ValidationError(
            '%(value)s não é um email institucional válido da UnB.',
            params={'value': value},
        )

# Novo UserManager customizado
class UsuarioPersonalizadoManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UsuarioPersonalizado(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[validate_unb_email] # <-- Adicione o validador aqui
    )
    username = None # Remove o campo username padrão
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email' # Usa o email como campo de login

    # Adicione o manager customizado
    objects = UsuarioPersonalizadoManager()

    def __str__(self):
        return self.email