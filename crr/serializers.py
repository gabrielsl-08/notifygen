# serializers.py
from rest_framework import serializers
from .models import Crr,TabelaArrendatario, Arrendatario, Ait, TabelaEnquadramento, Enquadramento  # exemplo de modelo

class CrrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crr
        fields = '__all__'  # Ou liste campos específicos ['campo1', 'campo2']

class TabelaArrendatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaArrendatario
        fields = '__all__'

class ArrendatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrendatario
        fields = '__all__'

class AitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ait
        fields = '__all__'

class TabelaEnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaEnquadramento
        fields = '__all__'

class EnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquadramento
        fields = '__all__'