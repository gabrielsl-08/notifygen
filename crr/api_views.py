
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from .models import Crr,Veiculo ,Condutor,TabelaEnquadramento,Ait, Enquadramento
from .serializers import (CrrSerializer,VeiculoSerializer,CondutorSerializer,TabelaEnquadramentoSerializer,AitSerializer, EnquadramentoSerializer)

from divprom.permissions import IsOwnerOfCrr


class CrrViewSet(viewsets.ModelViewSet):
    queryset = Crr.objects.all()
    serializer_class = CrrSerializer
    permission_classes = [DjangoModelPermissions,IsOwnerOfCrr]
    
    


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [DjangoModelPermissions]

class AitViewSet(viewsets.ModelViewSet):
    queryset = Ait.objects.all()
    serializer_class = AitSerializer
    permission_classes = [DjangoModelPermissions]

class CondutorViewSet(viewsets.ModelViewSet):
    queryset = Condutor.objects.all()
    serializer_class = CondutorSerializer
    permission_classes = [DjangoModelPermissions]

class TabelaEnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = TabelaEnquadramento.objects.all()
    serializer_class = TabelaEnquadramentoSerializer
    permission_classes = [DjangoModelPermissions]

class EnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = Enquadramento.objects.all()
    serializer_class = EnquadramentoSerializer
    permission_classes = [DjangoModelPermissions]

