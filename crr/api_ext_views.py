# views.py
from rest_framework.decorators import api_view, throttle_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from .models import Crr, Veiculo
from .serializers import ConsultaExterna
from rest_framework.permissions import AllowAny
from django.shortcuts import render

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def consulta_publica_crr(request):
    """
    Consulta pública de CRR por placa ou chassi.
    """
    placa = request.query_params.get('placa')
    chassi = request.query_params.get('chassi')
    
    if not placa and not chassi:
        return Response(
            {"erro": "Informe a placa ou o chassi para consulta."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Como o relacionamento é reverso, consultamos primeiro o Veiculo
    veiculo_queryset = Veiculo.objects.select_related('crr')  # Agora o select_related funciona
    
    if placa:
        veiculo_queryset = veiculo_queryset.filter(placa__iexact=placa.strip())
    elif chassi:
        veiculo_queryset = veiculo_queryset.filter(chassi__iexact=chassi.strip())
    
    # Verifica se encontrou o veículo
    veiculo = veiculo_queryset.first()
    if not veiculo:
        return Response(
            {"mensagem": "Veículo não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verifica se o veículo tem um CRR associado
    if not veiculo.crr:
        return Response(
            {"mensagem": "CRR não encontrado para este veículo."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serializa o CRR encontrado
    crr_instance = veiculo.crr
    serializer = ConsultaExterna(crr_instance)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

def pagina_consulta_crr(request):
    return render(request, 'crr/consulta_crr_api.html')