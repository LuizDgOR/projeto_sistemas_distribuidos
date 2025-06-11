from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class ProfilePermissionMiddleware:
    """
    Middleware para verificar permissões baseadas no perfil do usuário
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        
        response = self.get_response(request)
        return response
    
    def process_request(self, request):
        # Pular verificação para URLs de autenticação e admin
        exempt_urls = [
            '/admin/',
            '/login/',
            '/logout/',
            '/accounts/',
            '/monografias/',  # Permitir acesso à listagem
        ]
        
        # Verificar se a URL atual está isenta
        for exempt_url in exempt_urls:
            if request.path.startswith(exempt_url):
                return None
        
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            return None
        
        # Verificar se o usuário tem perfil
        if not hasattr(request.user, 'profile'):
            logger.warning(f"Usuário {request.user.username} sem perfil tentou acessar {request.path}")
            return self._render_403(request, "Usuário sem perfil definido.")
        
        # URLs que requerem permissão de gerenciamento
        admin_required_patterns = [
            '/monografias/nova/',
            '/monografias/criar/',
            '/editar/',
            '/excluir/',
            '/delete/',
        ]
        
        # Verificar se a URL requer permissões administrativas
        requires_admin = any(pattern in request.path for pattern in admin_required_patterns)
        
        if requires_admin and not request.user.profile.pode_gerenciar_monografias:
            logger.warning(f"Usuário {request.user.username} ({request.user.profile.get_tipo_usuario_display()}) tentou acessar {request.path}")
            return self._render_403(request, 
                f"Acesso negado. Seu perfil ({request.user.profile.get_tipo_usuario_display()}) não possui permissão para esta ação.")
        
        return None
    
    def _render_403(self, request, message="Acesso negado."):
        """Renderiza a página de erro 403 personalizada"""
        context = {
            'error_message': message,
            'user': request.user,
        }
        return render(request, 'errors/403.html', context, status=403)