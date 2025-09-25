from django.urls import path
from .views import (
    CadastroView, LoginView, PerfilView,
    PasswordResetRequestView, PasswordResetConfirmView
)

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='api-cadastro'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('perfil/', PerfilView.as_view(), name='api-perfil'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
]