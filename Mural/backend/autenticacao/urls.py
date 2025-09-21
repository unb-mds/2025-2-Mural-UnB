from django.urls import path
from .views import CadastroView, LoginView, PerfilView 

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='api-cadastro'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('perfil/', PerfilView.as_view(), name='api-perfil'),
]