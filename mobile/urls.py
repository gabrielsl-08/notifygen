from django.urls import path
from . import views

app_name = 'mobile'

urlpatterns = [
    path('criar_crr', views.criar_crr_mobile, name='criar_crr'),
   
    path('listar/', views.lista_crrs, name='lista_crrs'),
]
