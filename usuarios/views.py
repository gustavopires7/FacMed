from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from .forms import CadastroProfissionalForm, UsuarioCreationForm, UsuarioUpdateForm
from .models import Cidade, Especialidade, Profissional, Usuario


class IndexView(TemplateView):
    template_name = 'usuarios/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        nome = self.request.GET.get('nome', '').strip()
        
        profissionais = Profissional.objects.all()
        if nome:
            profissionais = profissionais.filter(usuario__username__icontains=nome)
        
        especialidade = self.request.GET.get('especialidade', '').strip()
        if especialidade:
            profissionais = profissionais.filter(especialidade_id=especialidade)
        
        paginator = Paginator(profissionais, 10)
        page_number = self.request.GET.get('page', 1)

        especialidades = Especialidade.objects.all()

        try:
            page_obj = paginator.get_page(page_number)
        except Exception:
            raise Http404("Página não encontrada")
        
        context["page_obj"] = page_obj
        context["profissionais"] = page_obj.object_list
        context["especialidades"] = especialidades
        context["is_paginated"] = page_obj.has_other_pages()
        return context

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

class ProfissionalDetalhesView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/profissional_detalhes.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca o profissional pelo ID fornecido na URL
        profissional_id = self.kwargs.get('pk')  # Assumindo que o ID é passado como parte da URL
        context['profissional'] = get_object_or_404(Profissional, pk=profissional_id)
        return context