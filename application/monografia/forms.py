from django import forms
from .models import Monografia
from .widgets import CustomClearableFileInput

class MonografiaForm(forms.ModelForm):
    class Meta:
        model = Monografia
        fields = [
            'titulo', 'autor', 'orientador', 'coorientador',
            'resumo', 'abstract', 'palavras_chave', 'data_defesa', 'arquivo'
        ]

        labels = {
            'arquivo': '',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'autor': forms.TextInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'orientador': forms.TextInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'coorientador': forms.TextInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'resumo': forms.Textarea(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'abstract': forms.Textarea(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'palavras_chave': forms.TextInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'data_defesa': forms.DateInput(attrs={'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500', 'type': 'date'}),
            'arquivo': CustomClearableFileInput(attrs={
                'class': 'border border-blue-300 rounded-0 p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            extensao = arquivo.name.split('.')[-1].lower()
            if extensao not in ['pdf']:
                raise forms.ValidationError("Formato de arquivo inválido. Utilize PDF")
        return arquivo
