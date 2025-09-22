# Mural/backend/autenticacao/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer
from .models import UsuarioPersonalizado
from rest_framework.permissions import IsAuthenticated

class CadastroView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data) # Cria um serializer que irá validar e salvar os dados
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Por favor, forneça email e senha.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password) # Aqui tenta autenticar o usuário

        if user:
            # Aqui você pode gerar e retornar um token (veremos isso no futuro)
            # Por agora, vamos retornar uma resposta de sucesso simples.
            return Response({'success': 'Login bem-sucedido!', 'user_id': user.id}, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

class PerfilView(APIView):
    permission_classes = [IsAuthenticated] # Garante que apenas usuários autenticados podem acessar

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# A view de logout em uma API geralmente é feita no frontend (apagando o token)
# mas podemos criar um endpoint se necessário no futuro.