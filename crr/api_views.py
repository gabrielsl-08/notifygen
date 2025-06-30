
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets
from .models import Crr,Veiculo ,Condutor,TabelaEnquadramento,Ait, Enquadramento
from .serializers import (CrrSerializer,VeiculoSerializer,CondutorSerializer,TabelaEnquadramentoSerializer,AitSerializer, EnquadramentoSerializer)
from .permissions import IsJavaUser



class CrrViewSet(viewsets.ModelViewSet):
    queryset = Crr.objects.all()
    serializer_class = CrrSerializer
    permission_classes = [IsJavaUser]
    
    


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsJavaUser]

class AitViewSet(viewsets.ModelViewSet):
    queryset = Ait.objects.all()
    serializer_class = AitSerializer
    permission_classes = [IsJavaUser]

class CondutorViewSet(viewsets.ModelViewSet):
    queryset = Condutor.objects.all()
    serializer_class = CondutorSerializer
    permission_classes = [IsJavaUser]

class TabelaEnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = TabelaEnquadramento.objects.all()
    serializer_class = TabelaEnquadramentoSerializer
    permission_classes = [IsJavaUser]

class EnquadramentoViewSet(viewsets.ModelViewSet):
    queryset = Enquadramento.objects.all()
    serializer_class = EnquadramentoSerializer
    permission_classes = [IsJavaUser]

