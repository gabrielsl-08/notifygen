from django.urls import path
from . import views

app_name = 'mobile'

urlpatterns = [
    path('novo/', views.criar_crr, name='criar_crr'),
    path('meus-crrs/', views.lista_crr, name='lista_crr'),
    path('imprimir/<int:pk>/', views.imprimir_crr, name='imprimir_crr'),
]
