# serializers.py
from rest_framework import serializers
from .models import (Crr, Ait,
                    TabelaEnquadramento, Enquadramento,AgenteAutuador,Condutor,
                    ) 


class AitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ait
        exclude = ['crr']


class CondutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condutor
        exclude = ['crr']


class EnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquadramento
        exclude = ['crr']


class AgenteAutuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenteAutuador
        fields = ['id', 'nome_agente', 'matricula', 'orgao']

class TabelaEnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaEnquadramento
        fields = '__all__'


class CrrSerializer(serializers.ModelSerializer):
    agente_autuador = serializers.PrimaryKeyRelatedField(queryset=AgenteAutuador.objects.all())
    condutor = CondutorSerializer(many=True)
    ait = AitSerializer(many=True)
    enquadramentos = EnquadramentoSerializer(many=True)

    class Meta:
        model = Crr
        fields = '__all__'

    def create(self, validated_data):
        condutores_data = validated_data.pop('condutores', [])
        aits_data = validated_data.pop('ait', [])
        enquadramentos_data = validated_data.pop('enquadramentos', [])

        crr = Crr.objects.create(**validated_data)

        for condutor in condutores_data:
            Condutor.objects.create(crr=crr, **condutor)

        for ait in aits_data:
            Ait.objects.create(crr=crr, **ait)

        for enquadramento in enquadramentos_data:
            Enquadramento.objects.create(crr=crr, **enquadramento)

        return crr

    def update(self, instance, validated_data):
        condutores_data = validated_data.pop('condutores', [])
        aits_data = validated_data.pop('ait', [])
        enquadramentos_data = validated_data.pop('enquadramentos', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Limpa e recria relacionados
        instance.condutores.all().delete()
        instance.ait.all().delete()
        instance.enquadramentos.all().delete()

        for condutor in condutores_data:
            Condutor.objects.create(crr=instance, **condutor)

        for ait in aits_data:
            Ait.objects.create(crr=instance, **ait)

        for enquadramento in enquadramentos_data:
            Enquadramento.objects.create(crr=instance, **enquadramento)

        return instance
