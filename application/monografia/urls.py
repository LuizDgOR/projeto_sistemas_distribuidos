from django.urls import path
from . import views

app_name = 'monografia'

urlpatterns = [
    path('', views.MonografiaListView.as_view(), name='list'),
    path('criar/', views.MonografiaCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MonografiaDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.MonografiaUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.MonografiaDeleteView.as_view(), name='delete'),
]
