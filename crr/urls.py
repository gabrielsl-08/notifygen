# crr/urls.py
from django.urls import path
from .views import (criar_crr,listar_crr, triagem_crr,revisar_crr, detalhar_crr,gerar_pdf_crr,
                    alterar_status_crr, gerar_edital_view                    
                    )

urlpatterns = [
    path('admin/crr/', criar_crr, name='criar_crr'),
    path('admin/crr/listar/', listar_crr, name='listar_crr'),
    path('admin/crr/triagem/', triagem_crr, name='triagem_crr'),
    path('crr/<int:pk>/revisar/', revisar_crr, name='revisar_crr'),  
    path('admin/crr/<int:pk>/', detalhar_crr, name='detalhar_crr'),
    path('admin/crr/<int:pk>/pdf/', gerar_pdf_crr, name='gerar_pdf_crr'),
    path('gerar-edital/', gerar_edital_view, name='gerar_edital'),
    path('crr/alterar-status/', alterar_status_crr, name='alterar_status_crr'),
  
    
    # Adicione outras URLs como listagem, detalhes, etc.
]
