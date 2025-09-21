from rest_framework import serializers
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