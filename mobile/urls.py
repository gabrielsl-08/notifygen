from django.urls import path
from . import views


urlpatterns = [
  

    path('criar_crr', views.criar_crr_mobile, name='criar_crr'),
    path('listar/', views.lista_crrs, name='lista_crrs'),
    path('crr/imprimir/<int:crr_id>/', views.imprimir_crr, name='imprimir_crr'),
    
]
