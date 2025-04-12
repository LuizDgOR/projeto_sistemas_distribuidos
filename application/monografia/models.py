from django.db import models

class Monografia(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    orientador = models.CharField(max_length=255)
    coorientador = models.CharField(max_length=255)
    resumo = models.TextField()
    abstract = models.TextField()
    palavras_chave = models.CharField(max_length=255, help_text="Separe as palavras por vírgula")
    data_defesa = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    arquivo = models.FileField(upload_to='monografias/')

    def __str__(self):
        return self.titulo

