from django.urls import path
from .views import (
    IndexView, 
    UserRegisterView, 
    UserLoginView, 
    UserLogoutView, 
    ProfileView, 
    ProfileEditView, 
    ProfileDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registrar/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('perfil/', ProfileView.as_view(), name='profile'),
    path('perfil/editar/', ProfileEditView.as_view(), name='profile_edit'),
    path('perfil/excluir/', ProfileDeleteView.as_view(), name='profile_delete'),
]