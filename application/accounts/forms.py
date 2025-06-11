from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Senha'
        })
    )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'seu@email.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Sobrenome'
        })
    )
    
    tipo_usuario = forms.ChoiceField(
        choices=UserProfile.TIPOS_USUARIO,
        required=True,
        initial='aluno',
        widget=forms.Select(attrs={
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar classes CSS aos campos herdados
        self.fields['username'].widget.attrs.update({
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Nome de usuário'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Senha'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'border border-blue-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirmar senha'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar ou atualizar o perfil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.tipo_usuario = self.cleaned_data['tipo_usuario']
            profile.save()
        return user