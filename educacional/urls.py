from django.urls import path

from . import views

app_name = 'educacional'

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('resultado/<int:pk>/', views.resultado_view, name='resultado'),
    path('estatisticas/', views.estatisticas_view, name='estatisticas'),
]
