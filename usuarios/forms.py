from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Endereco, Estado, Cidade

class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(required=False)
    data_nascimento = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Campos para endereço
    logradouro = forms.CharField(max_length=200, required=False)
    numero = forms.CharField(max_length=20, required=False)
    complemento = forms.CharField(max_length=100, required=False)
    cep = forms.CharField(max_length=10, required=False)
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(), 
        required=False
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(), 
        required=False
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'telefone', 'data_nascimento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cidade'].queryset = Cidade.objects.none()

        # Se um estado for selecionado, atualiza as cidades disponíveis
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(estado_id=estado_id)
            except (ValueError, TypeError):
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Salva informações do usuário
        user.email = self.cleaned_data['email']
        user.telefone = self.cleaned_data['telefone']
        user.data_nascimento = self.cleaned_data['data_nascimento']
        
        if commit:
            user.save()
            
            # Cria endereço se todos os campos estiverem preenchidos
            if all([
                self.cleaned_data.get('logradouro'),
                self.cleaned_data.get('cep'),
                self.cleaned_data.get('estado'),
                self.cleaned_data.get('cidade')
            ]):
                endereco = Endereco.objects.create(
                    logradouro=self.cleaned_data['logradouro'],
                    numero=self.cleaned_data['numero'],
                    complemento=self.cleaned_data['complemento'],
                    cep=self.cleaned_data['cep'],
                    cidade=self.cleaned_data['cidade'],
                    estado=self.cleaned_data['estado']
                )
                user.endereco = endereco
                user.save()
        
        return user

class UsuarioUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(required=False)
    data_nascimento = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Campos para endereço
    logradouro = forms.CharField(max_length=200, required=False)
    numero = forms.CharField(max_length=20, required=False)
    complemento = forms.CharField(max_length=100, required=False)
    cep = forms.CharField(max_length=10, required=False)
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(), 
        required=False
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(), 
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['email', 'telefone', 'data_nascimento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Preenche campos iniciais se usuário já tem endereço
        if self.instance.endereco:
            self.fields['logradouro'].initial = self.instance.endereco.logradouro
            self.fields['numero'].initial = self.instance.endereco.numero
            self.fields['complemento'].initial = self.instance.endereco.complemento
            self.fields['cep'].initial = self.instance.endereco.cep
            self.fields['estado'].initial = self.instance.endereco.estado
            self.fields['cidade'].initial = self.instance.endereco.cidade

            # Atualiza cidades de acordo com o estado
            self.fields['cidade'].queryset = Cidade.objects.filter(estado=self.instance.endereco.estado)
        else:
            self.fields['cidade'].queryset = Cidade.objects.none()

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Salva informações do usuário
        user.email = self.cleaned_data['email']
        user.telefone = self.cleaned_data['telefone']
        user.data_nascimento = self.cleaned_data['data_nascimento']
        
        if commit:
            user.save()
            
            # Atualiza ou cria endereço
            if all([
                self.cleaned_data.get('logradouro'),
                self.cleaned_data.get('cep'),
                self.cleaned_data.get('estado'),
                self.cleaned_data.get('cidade')
            ]):
                # Se já existe endereço, atualiza
                if user.endereco:
                    endereco = user.endereco
                    endereco.logradouro = self.cleaned_data['logradouro']
                    endereco.numero = self.cleaned_data['numero']
                    endereco.complemento = self.cleaned_data['complemento']
                    endereco.cep = self.cleaned_data['cep']
                    endereco.cidade = self.cleaned_data['cidade']
                    endereco.estado = self.cleaned_data['estado']
                    endereco.save()
                else:
                    # Se não existe, cria novo endereço
                    endereco = Endereco.objects.create(
                        logradouro=self.cleaned_data['logradouro'],
                        numero=self.cleaned_data['numero'],
                        complemento=self.cleaned_data['complemento'],
                        cep=self.cleaned_data['cep'],
                        cidade=self.cleaned_data['cidade'],
                        estado=self.cleaned_data['estado']
                    )
                    user.endereco = endereco
                    user.save()
        
        return user