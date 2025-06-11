from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from functools import wraps

def pode_gerenciar_monografias(view_func):
    """Decorador que verifica se o usuário pode gerenciar monografias"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Verifica se o usuário tem perfil e pode gerenciar monografias
        if not hasattr(request.user, 'profile') or not request.user.profile.pode_gerenciar_monografias():
            return render(request, 'errors/403.html', {
                'error_message': 'Você não tem permissão para realizar esta ação. Apenas Administradores, Professores e Coordenadores podem gerenciar monografias.',
                'user_type': request.user.profile.get_tipo_usuario_display() if hasattr(request.user, 'profile') else 'Usuário sem perfil'
            }, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view