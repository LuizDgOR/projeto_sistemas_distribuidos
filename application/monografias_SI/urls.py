"""
URL configuration for projeto_sistemas_distribuidos project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from accounts.views import dashboard_view, logout_view
from django.shortcuts import render

def custom_403_view(request, exception=None):
    """View personalizada para erro 403"""
    return render(request, 'errors/403.html', status=403)

def custom_404_view(request, exception=None):
    """View personalizada para erro 404"""
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    """View personalizada para erro 500"""
    return render(request, 'errors/500.html', status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('monografias/', include('monografia.urls')),
    path('', RedirectView.as_view(url='/monografias/', permanent=False), name='home'),
    
    # URLs de autenticação diretas
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('dashboard/', dashboard_view, name='dashboard'),
]

# Configurar handlers de erro
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customização do admin
admin.site.site_header = "Administração - Sistema de Monografias"
admin.site.site_title = "Admin Monografias"
admin.site.index_title = "Painel de Administração"