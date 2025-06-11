from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm
from django.db.models import Count
from monografia.models import Monografia
from .models import UserProfile, UserAuditLog

class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            auth_user = authenticate(request, username=username, password=password)
            
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, f'Bem-vindo, {auth_user.get_full_name() or auth_user.username}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Credenciais inválidas.')
        
        return render(request, self.template_name, {'form': form})

def logout_view(request):
    """View personalizada para logout"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'Até logo, {user_name}! Logout realizado com sucesso.')
    return redirect('monografia:list')

@login_required  
def dashboard_view(request):
    """View para o dashboard do usuário"""
    return redirect('accounts:dashboard')

@login_required
def profile(request):
    """Perfil do usuário"""
    if request.method == 'POST':
        # Atualizar informações básicas do usuário
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        
        # Log da atualização
        UserAuditLog.objects.create(
            user=request.user,
            action=UserAuditLog.ACTION_UPDATE,
            object_type='profile',
            ip_address=get_client_ip(request),
            details='Atualização de perfil'
        )
        
        return redirect('accounts:profile')
    
    # Buscar logs de atividade do usuário
    recent_activities = UserAuditLog.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:10]
    
    return render(request, 'accounts/profile.html', {
        'recent_activities': recent_activities
    })

def get_client_ip(request):
    """Obter IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return redirect('accounts:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar conta. Verifique os dados informados.')
        return super().form_invalid(form)

@login_required
def dashboard(request):
    """
    Dashboard personalizado baseado no tipo de usuário
    """
    user = request.user
    profile = getattr(user, 'profile', None)
    
    context = {
        'user': user,
        'profile': profile,
    }
    
    # Estatísticas gerais
    context['total_monografias'] = Monografia.objects.count()
    
    # Estatísticas específicas por tipo de usuário
    if profile:
        if profile.is_professor():
            context['minhas_orientacoes'] = Monografia.objects.filter(orientador__icontains=user.get_full_name()).count()
            context['minhas_coorientacoes'] = Monografia.objects.filter(coorientador__icontains=user.get_full_name()).count()
            
        elif profile.is_aluno():
            context['minhas_monografias'] = Monografia.objects.filter(autor__icontains=user.get_full_name()).count()
            
        elif profile.is_admin():
            from django.contrib.auth.models import User
            context['total_usuarios'] = User.objects.count()
    
    # Monografias recentes
    context['monografias_recentes'] = Monografia.objects.order_by('-created_at')[:5]
    
    return render(request, 'accounts/dashboard.html', context)
