from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Monografia
from .serializers import MonografiaSerializer

class MonografiaViewSet(viewsets.ModelViewSet):
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer

    # autenticação e permissão
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # upload de arquivo
    parser_classes = [MultiPartParser, FormParser]

    # filtros e buscas , ordenação
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['orientador', 'coorientador', 'data_defesa']
    search_fields = ['titulo', 'resumo', 'abstract', 'palavras_chave']
    ordering_fields = ['data_defesa', 'titulo']
    ordering = ['-created_at']
