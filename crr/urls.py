# crr/urls.py
from django.urls import path
from .views import criar_crr

urlpatterns = [
    path('crr/novo/', criar_crr, name='criar_crr'),
    
    # Adicione outras URLs como listagem, detalhes, etc.
]
