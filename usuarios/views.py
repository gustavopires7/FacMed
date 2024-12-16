from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Cidade

from django.http import HttpResponseRedirect
from .forms import  UsuarioUpdateForm, CadastroProfissionalForm, UsuarioCreationForm
from .models import Usuario, Profissional

class IndexView(TemplateView):
    template_name = 'usuarios/index.html'

class UserRegisterView(CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/cliente_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

class ProfessionalRegisterView(CreateView):
    model = Profissional
    form_class = CadastroProfissionalForm
    template_name = 'usuarios/profissional_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print(form.errors)
        form.save()
        return HttpResponseRedirect(self.success_url)

class UserLoginView(TemplateView):
    template_name = 'usuarios/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {'error': 'Credenciais inválidas'})

class UserLogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/profile.html'
    login_url = 'login'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('profile')
    login_url = 'login'

    def get_object(self, queryset=None):
        return self.request.user

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('login')
    login_url = 'login'

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)


def tipo_usuario(request):
    return render(request, 'usuarios/selecao_usuario.html')


def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).values('id', 'nome')
    return JsonResponse(list(cidades), safe=False)
