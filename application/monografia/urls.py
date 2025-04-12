from django.urls import path
from .views import (
    MonografiaCreateView,
    MonografiaListView,
    MonografiaDetailView,
    MonografiaUpdateView,
    MonografiaDeleteView,
)

urlpatterns = [
    path('', MonografiaListView.as_view(), name='monografia_list'),
    path('criar/', MonografiaCreateView.as_view(), name='monografia_create'),
    path('<int:pk>/', MonografiaDetailView.as_view(), name='monografia_detail'),
    path('<int:pk>/editar/', MonografiaUpdateView.as_view(), name='monografia_update'),
    path('<int:pk>/excluir/', MonografiaDeleteView.as_view(), name='monografia_delete'),
]
