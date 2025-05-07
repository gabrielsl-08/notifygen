# serializers.py
from rest_framework import serializers
from .models import (Crr,TabelaArrendatario, Arrendatario, Ait,
                    TabelaEnquadramento, Enquadramento,AgenteAutuador,Condutor,
                    ) 


class AgenteAutuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenteAutuador
        fields =  fields = '__all__'

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

class CondutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condutor
        fields =  '__all__'

class CrrSerializer(serializers.ModelSerializer):
    agente_autuador = AgenteAutuadorSerializer()
    condutor = CondutorSerializer(many=True)
    ait = AitSerializer(many=True)
    enquadramentos = EnquadramentoSerializer(many=True)
    class Meta:
        model = Crr
        fields = '__all__'  # Ou liste campos específicos ['campo1', 'campo2']
