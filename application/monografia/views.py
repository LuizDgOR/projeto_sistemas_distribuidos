from django.urls import reverse_lazy
from django.db import models
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Monografia
from .forms import MonografiaForm
from .decorators import pode_gerenciar_monografias
from django.utils.decorators import method_decorator

# Mixin para verificar permissões
class PermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not hasattr(request.user, 'profile') or not request.user.profile.pode_gerenciar_monografias():
            raise PermissionDenied("Você não tem permissão para realizar esta ação.")
        
        return super().dispatch(request, *args, **kwargs)

# Listagem - acesso público
class MonografiaListView(ListView):
    model = Monografia
    template_name = 'monografias/monografia_list.html'  # Corrigir o nome do template
    context_object_name = 'monografias'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

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
            queryset = queryset.filter(
                models.Q(resumo__icontains=resumo_abstract) | 
                models.Q(abstract__icontains=resumo_abstract)
            )
        
        order_by = self.request.GET.get('order_by')
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_monografias'] = self.get_queryset().count()
        context['can_manage'] = (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'profile') and 
            self.request.user.profile.pode_gerenciar_monografias()
        )
        return context

# Detalhes - acesso público
class MonografiaDetailView(DetailView):
    model = Monografia
    template_name = 'monografias/monografia_detail.html'
    context_object_name = 'monografia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_manage'] = (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'profile') and 
            self.request.user.profile.pode_gerenciar_monografias()
        )
        return context

# Criar - apenas usuários com permissão
class MonografiaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografias/monografia_form.html'
    success_url = reverse_lazy('monografia:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Nova Monografia'
        context['button_text'] = 'Adicionar'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Monografia adicionada com sucesso!')
        return super().form_valid(form)

# Atualizar - apenas usuários com permissão
class MonografiaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografias/monografia_form.html'
    
    def get_success_url(self):
        return reverse_lazy('monografia:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Monografia'
        context['button_text'] = 'Atualizar'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Monografia atualizada com sucesso!')
        return super().form_valid(form)

# Deletar - apenas usuários com permissão
class MonografiaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Monografia
    template_name = 'monografias/monografia_confirm_delete.html'
    success_url = reverse_lazy('monografia:list')
    context_object_name = 'monografia'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Monografia "{self.get_object().titulo}" deletada com sucesso!')
        return super().delete(request, *args, **kwargs)
