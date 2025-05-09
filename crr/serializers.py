# serializers.py
from rest_framework import serializers
from .models import (
    Crr, Ait, Condutor, Enquadramento, AgenteAutuador,
    TabelaEnquadramento
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
    condutores = CondutorSerializer(many=True)
    ait = AitSerializer(many=True)
    enquadramentos = EnquadramentoSerializer(many=True)
    agente_autuador = serializers.PrimaryKeyRelatedField(queryset=AgenteAutuador.objects.all())

    class Meta:
        model = Crr
        fields = '__all__'

    def create(self, validated_data):
        # Nested related data
        condutores_data = validated_data.pop('condutores', [])
        aits_data = validated_data.pop('ait', [])
        enquadramentos_data = validated_data.pop('enquadramentos', [])

        # Gera numero_crr automaticamente
        if not validated_data.get('numero_crr'):
            validated_data['numero_crr'] = gerar_numero_crr_mobile()

        crr = Crr.objects.create(**validated_data)

        # Condutores
        for condutor in condutores_data:
            Condutor.objects.create(crr=crr, **condutor)

        # AIT
        for ait in aits_data:
            Ait.objects.create(crr=crr, **ait)

        # Enquadramentos
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

        # Atualiza condutores
        instance.condutores.all().delete()
        for condutor in condutores_data:
            Condutor.objects.create(crr=instance, **condutor)

        # Atualiza AITs
        instance.ait.all().delete()
        for ait in aits_data:
            Ait.objects.create(crr=instance, **ait)

        # Atualiza enquadramentos
        instance.enquadramentos.all().delete()
        for enquadramento in enquadramentos_data:
            Enquadramento.objects.create(crr=instance, **enquadramento)

        return instance


def gerar_numero_crr_mobile():
    prefixo = "E-"
    ultimo_crr = Crr.objects.filter(numero_crr__startswith=prefixo).order_by('-numero_crr').first()
    if ultimo_crr and ultimo_crr.numero_crr:
        try:
            ultimo_num = int(ultimo_crr.numero_crr.replace(prefixo, ""))
        except ValueError:
            ultimo_num = 0
    else:
        ultimo_num = 0
    proximo_num = ultimo_num + 1
    return f"{prefixo}{str(proximo_num).zfill(2)}"
