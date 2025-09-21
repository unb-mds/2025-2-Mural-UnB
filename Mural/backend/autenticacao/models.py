from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.email