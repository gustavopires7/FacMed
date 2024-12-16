from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Endereco, Estado, Cidade, Profissional, Especialidade

class UsuarioCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(estado_id=estado_id)
            except (ValueError, TypeError):
                self.fields['cidade'].queryset = Cidade.objects.none()
        elif self.instance.pk:
            self.fields['cidade'].queryset = Cidade.objects.filter(estado=self.instance.estado)


    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'})
    )
    first_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        label='Confirmar Senha'
    )
    
    # Campos do usuário adicionais
    telefone = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'})
    )
    data_nascimento = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # Campos de endereço
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_estado'}),
        required=False
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_cidade'}),
        required=False
    )
    rua = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'})
    )
    numero = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'})
    )
    bairro = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'})
    )
    cep = forms.CharField(
        max_length=8, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'telefone', 'estado', 'cidade', 'rua', 'numero', 'bairro', 'telefone', 'cep', 'data_nascimento']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Verificar se as senhas coincidem
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

    def save(self):
        endereco = None
        if any([
            self.cleaned_data.get('estado'), 
            self.cleaned_data.get('cidade'), 
            self.cleaned_data.get('rua'), 
            self.cleaned_data.get('numero'), 
            self.cleaned_data.get('bairro'), 
            self.cleaned_data.get('cep')
        ]):


            endereco = Endereco.objects.create(
                cidade=self.cleaned_data.get('cidade'),
                rua=self.cleaned_data.get('rua'),
                numero=self.cleaned_data.get('numero'),
                bairro=self.cleaned_data.get('bairro'),
                cep=self.cleaned_data.get('cep')
            )

        # Criar usuário
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            telefone=self.cleaned_data.get('telefone'),
            data_nascimento=self.cleaned_data.get('data_nascimento'),            endereco=endereco  # Associa o endereço ao usuário
        )

        return usuario

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
    

class CadastroProfissionalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(estado_id=estado_id)
            except (ValueError, TypeError):
                self.fields['cidade'].queryset = Cidade.objects.none()
        elif self.instance.pk:
            self.fields['cidade'].queryset = Cidade.objects.filter(estado=self.instance.estado)


    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'})
    )
    first_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        label='Confirmar Senha'
    )
    telefone = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'})
    )
    data_nascimento = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    CRM = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número do CRM'})
    )
    especialidade = forms.ModelChoiceField(
        queryset=Especialidade.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    biografia = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Breve biografia'})
    )
    preco_servico = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Valor do serviço'})
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_estado'}),
        required=False
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_cidade'}),
        required=False
    )
    rua = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'})
    )
    numero = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'})
    )
    bairro = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'})
    )
    cep = forms.CharField(
        max_length=8, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'})
    )

    class Meta:
        model = Profissional
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'telefone', 'CRM', 'especialidade', 'biografia', 'preco_servico', 'estado', 'cidade', 'rua', 'numero', 'bairro', 'telefone', 'cep', 'data_nascimento']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está cadastrado.')
        return username


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Verificar se as senhas coincidem
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean_CRM(self):
        crm = self.cleaned_data.get('CRM')
        if crm and Profissional.objects.filter(CRM=crm).exists():
            raise forms.ValidationError('O CRM informado já está em uso.')
        return crm

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and not telefone.isdigit():
            raise forms.ValidationError('O telefone deve conter apenas números.')
        return telefone

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep and (len(cep) != 8 or not cep.isdigit()):
            raise forms.ValidationError('O CEP deve conter 8 dígitos numéricos.')
        return cep

    def clean_preco_servico(self):
        preco = self.cleaned_data.get('preco_servico')
        if preco and preco <= 0:
            raise forms.ValidationError('O preço do serviço deve ser maior que zero.')
        return preco

    def save(self):
        endereco = None
        if any([
            self.cleaned_data.get('estado'), 
            self.cleaned_data.get('cidade'), 
            self.cleaned_data.get('rua'), 
            self.cleaned_data.get('numero'), 
            self.cleaned_data.get('bairro'), 
            self.cleaned_data.get('cep')
        ]):
            
        

            endereco = Endereco.objects.create(
                cidade=self.cleaned_data.get('cidade'),
                rua=self.cleaned_data.get('rua'),
                numero=self.cleaned_data.get('numero'),
                bairro=self.cleaned_data.get('bairro'),
                cep=self.cleaned_data.get('cep')
            )

        usuario = Usuario.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            telefone=self.cleaned_data.get('telefone'),
            data_nascimento=self.cleaned_data.get('data_nascimento'),
            endereco=endereco
        )

        profissional = Profissional.objects.create(
            usuario=usuario,
            CRM=self.cleaned_data.get('CRM'),
            especialidade=self.cleaned_data.get('especialidade'),
            biografia=self.cleaned_data.get('biografia'),
            preco_servico=self.cleaned_data.get('preco_servico'),
        )

        return profissional
