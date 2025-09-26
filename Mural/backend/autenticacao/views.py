# Mural/backend/autenticacao/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer
from .models import UsuarioPersonalizado
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

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


# Endpoint para solicitar reset de senha.
# Recebe email, gera token e uid, envia email com link de redefinição.
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UsuarioPersonalizado.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Gerando o token:
            token = default_token_generator.make_token(user)
            reset_url = f"{request.build_absolute_uri('/')}autenticacao/password-reset-confirm/?uid={uid}&token={token}"
            send_mail(
                'Redefinição de senha',
                f'Use este link para redefinir sua senha: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return Response({'detail': 'Email de redefinição enviado.'})
        return Response(serializer.errors, status=400)


# Endpoint para confirmar o reset de senha.
# Recebe uid, token e nova senha, valida o token e redefine a senha do usuário.
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = UsuarioPersonalizado.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UsuarioPersonalizado.DoesNotExist):
                return Response({'error': 'Link inválido.'}, status=400)
            # Validando o token:
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Senha redefinida com sucesso.'})
            else:
                return Response({'error': 'Token inválido.'}, status=400)
        return Response(serializer.errors, status=400)

