from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import UsuarioPersonalizado

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # O DRF chama este método para criar um novo usuário
        # O método create_user garante que a senha seja hasheada corretamente
        user = UsuarioPersonalizado.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Serializer para solicitar reset de senha.
# Valida se o email existe no sistema.
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not UsuarioPersonalizado.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este email não existe.")
        return value

# Serializer para confirmar o reset de senha.
# Recebe uid, token e nova senha.
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)