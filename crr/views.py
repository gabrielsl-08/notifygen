
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets
from .models import Crr,TabelaArrendatario, Arrendatario, Ait, TabelaEnquadramento, Enquadramento
from .serializers import (CrrSerializer, TabelaArrendatarioSerializer,
                          ArrendatarioSerializer, AitSerializer,
                          TabelaEnquadramentoSerializer, EnquadramentoSerializer)

class CrrViewSet(viewsets.ModelViewSet):
    queryset = Crr.objects.all()
    serializer_class = CrrSerializer
    permission_classes = [DjangoModelPermissions]
    

class TabelaArrendatarioViewSet(viewsets.ModelViewSet):
    queryset = TabelaArrendatario.objects.all()
    serializer_class = TabelaArrendatarioSerializer
    permission_classes = [DjangoModelPermissions]

class ArrendatarioViewSet(viewsets.ModelViewSet):
    queryset = Arrendatario.objects.all()
    serializer_class = ArrendatarioSerializer
    permission_classes = [DjangoModelPermissions]

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