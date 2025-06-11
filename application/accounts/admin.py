from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserAuditLog

# Inline para o perfil do usuário
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'user'

# Estender o UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_tipo_usuario', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'profile__tipo_usuario')
    
    def get_tipo_usuario(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.get_tipo_usuario_display()
        return 'Sem perfil'
    get_tipo_usuario.short_description = 'Tipo de Usuário'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'is_locked', 'failed_login_attempts')
    list_filter = ('tipo_usuario', 'is_locked')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

@admin.register(UserAuditLog)
class UserAuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address', 'object_type')
    list_filter = ('action', 'timestamp', 'object_type')
    search_fields = ('user__username', 'details')
    readonly_fields = ('timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
