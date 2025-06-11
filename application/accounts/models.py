from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    TIPOS_USUARIO = [
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('coordenador', 'Coordenador'),
        ('aluno', 'Aluno'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tipo_usuario = models.CharField(
        'Tipo de usuário',
        max_length=20,
        choices=TIPOS_USUARIO,
        default='aluno'
    )
    
    # Campos adicionais para auditoria
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_tipo_usuario_display()})"

    def pode_gerenciar_monografias(self):
        """Verifica se o usuário pode adicionar/editar/deletar monografias"""
        return self.tipo_usuario in ['admin', 'professor', 'coordenador']

    def is_admin(self):
        return self.tipo_usuario == 'admin'

    def is_professor(self):
        return self.tipo_usuario == 'professor'

    def is_coordenador(self):
        return self.tipo_usuario == 'coordenador'

    def is_aluno(self):
        return self.tipo_usuario == 'aluno'

class UserAuditLog(models.Model):
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_VIEW = 'view'
    ACTION_FAILED_LOGIN = 'failed_login'

    ACTION_CHOICES = [
        (ACTION_LOGIN, 'Login'),
        (ACTION_LOGOUT, 'Logout'),
        (ACTION_CREATE, 'Criar'),
        (ACTION_UPDATE, 'Atualizar'),
        (ACTION_DELETE, 'Excluir'),
        (ACTION_VIEW, 'Visualizar'),
        (ACTION_FAILED_LOGIN, 'Tentativa de Login Falhada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    object_type = models.CharField(max_length=50, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

# Signal para criar perfil automaticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
