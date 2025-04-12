from django.urls import reverse_lazy
from django.db import models
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Monografia
from .forms import MonografiaForm

#criar
class MonografiaCreateView(CreateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografias/monografia_form.html'
    success_url = reverse_lazy('monografia_list')

#listar
class MonografiaListView(ListView):
    model = Monografia
    template_name = 'monografias/monografia_list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        titulo = self.request.GET.get('titulo')
        orientador = self.request.GET.get('orientador')
        coorientador = self.request.GET.get('coorientador')
        palavra = self.request.GET.get('palavra')
        data_defesa = self.request.GET.get('data_defesa')
        resumo_abstract = self.request.GET.get('texto')

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if orientador:
            queryset = queryset.filter(orientador__icontains=orientador)
        if coorientador:
            queryset = queryset.filter(coorientador__icontains=coorientador)
        if palavra:
            queryset = queryset.filter(palavras_chave__icontains=palavra)
        if data_defesa:
            queryset = queryset.filter(data_defesa=data_defesa)
        if resumo_abstract:
            queryset = queryset.filter(models.Q(resumo__icontains=resumo_abstract) | models.Q(abstract__icontains=resumo_abstract))
        
        order_by = self.request.GET.get('order_by')
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset

#detalhes
class MonografiaDetailView(DetailView):
    model = Monografia
    template_name = 'monografias/monografia_detail.html'

#atualiza
class MonografiaUpdateView(UpdateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografias/monografia_form.html'
    success_url = reverse_lazy('monografia_list')

#excluir
class MonografiaDeleteView(DeleteView):
    model = Monografia
    template_name = 'monografias/monografia_confirm_delete.html'
    success_url = reverse_lazy('monografia_list')
