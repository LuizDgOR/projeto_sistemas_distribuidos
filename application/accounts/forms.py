from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Senha'
        })
    )

# Deixaremos UserRegistrationForm para depois, quando o modelo User estiver funcionando