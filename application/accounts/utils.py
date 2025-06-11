from django.utils import timezone
from .models import UserAuditLog

def get_client_ip(request):
    """Obtém o IP do cliente da requisição"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_user_action(request, user, action, object_type=None, object_id=None, details=None):
    """Registra ação do usuário para auditoria"""
    UserAuditLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        object_type=object_type or '',
        object_id=object_id,
        details=details or ''
    )