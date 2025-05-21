
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets
from .models import Crr, Ait, TabelaEnquadramento, Enquadramento,Condutor
from .serializers import (CrrSerializer, AitSerializer,TabelaEnquadramentoSerializer, EnquadramentoSerializer,CondutorSerializer)

from divprom.divprom.permissions import IsOwnerOfCrr


class CrrViewSet(viewsets.ModelViewSet):
    queryset = Crr.objects.all()
    serializer_class = CrrSerializer
    permission_classes = [DjangoModelPermissions,IsOwnerOfCrr]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'agenteAutuador'):
            return Crr.objects.filter(agenteAutuador__usuario=self.request.user)
        return Crr.objects.none()



class AitViewSet(viewsets.ModelViewSet):
    queryset = Ait.objects.all()
    serializer_class = AitSerializer
    permission_classes = [DjangoModelPermissions]

class TabelaEnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = TabelaEnquadramento.objects.all()
    serializer_class = TabelaEnquadramentoSerializer
    permission_classes = [DjangoModelPermissions]

class EnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = Enquadramento.objects.all()
    serializer_class = EnquadramentoSerializer
    permission_classes = [DjangoModelPermissions]

class CondutorViewSet(viewsets.ModelViewSet):
    queryset = Condutor.objects.all()
    serializer_class = EnquadramentoSerializer
    permission_classes = [DjangoModelPermissions]