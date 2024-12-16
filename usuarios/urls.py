from django.urls import path
from .views import (
    IndexView, 
    UserRegisterView, 
    UserLoginView, 
    UserLogoutView, 
    ProfileView, 
    ProfileEditView, 
    ProfileDeleteView,
    ProfessionalRegisterView,
    tipo_usuario,
    carregar_cidades,   
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
]