from django.urls import path

from .views import (
    IndexView,
    ProfessionalRegisterView,
    ProfileDeleteView,
    ProfileEditView,
    ProfileView,
    ProfissionalDetalhesView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    carregar_cidades,
    tipo_usuario,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('usuario/tipo/', tipo_usuario, name='tipo_usuario'),
    path('cadastro/cliente/', UserRegisterView.as_view(), name='register_client'),
    path('cadastro/profissional/', ProfessionalRegisterView.as_view(), name='register_professional'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('perfil/', ProfileView.as_view(), name='profile'),
    path('perfil/editar/', ProfileEditView.as_view(), name='profile_edit'),
    path('perfil/excluir/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('carregar-cidades/', carregar_cidades, name='carregar_cidades'),
    path('profissional/detalhes/<int:pk>/', ProfissionalDetalhesView.as_view(), name='profissional_detalhes'),
]