# serializers.py
from rest_framework import serializers
from .models import (
    Crr, Ait,Veiculo ,Condutor, Enquadramento, AgenteAutuador,
    TabelaEnquadramento
)


class AitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ait
        exclude = ['crr']

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        exclude = ['crr']

class CondutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condutor
        exclude = ['crr']


class EnquadramentoSerializer(serializers.ModelSerializer):
    enquadramento = serializers.SlugRelatedField(
        slug_field='codigo',
        queryset=TabelaEnquadramento.objects.all()
    )
    class Meta:
        model = Enquadramento
        exclude = ['crr']

class AgenteAutuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenteAutuador
        fields = '__all__'


class TabelaEnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaEnquadramento
        fields = '__all__'


class CrrSerializer(serializers.ModelSerializer):
    veiculo = VeiculoSerializer()
    condutores = CondutorSerializer(many=True)
    aits = AitSerializer(many=True)
    enquadramentos = EnquadramentoSerializer(many=True)
    agenteAutuador = serializers.PrimaryKeyRelatedField(queryset=AgenteAutuador.objects.all())

    class Meta:
        model = Crr
        fields = '__all__'

    

    



