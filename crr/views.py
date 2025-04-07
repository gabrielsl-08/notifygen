from django.shortcuts import render
from .models import NumeroEdital

# Recupera ou cria o primeiro número de edital
numero_edital, created = NumeroEdital.objects.get_or_create(id=1)

# Usa o número atual
numero_atual = numero_edital.numero

# Incrementa para o próximo uso
numero_edital.incrementar()
