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
    veiculo = VeiculoSerializer(many=True)
    condutores = CondutorSerializer(many=True)
    aits = AitSerializer(many=True)
    enquadramentos = EnquadramentoSerializer(many=True)
    agenteAutuador = serializers.PrimaryKeyRelatedField(queryset=AgenteAutuador.objects.all())

    class Meta:
        model = Crr
        fields = '__all__'

    def create(self, validated_data):
        # Extrai dados aninhados
        veiculo_data = validated_data.pop('veiculo', [])
        condutores_data = validated_data.pop('condutores', [])
        aits_data = validated_data.pop('aits', [])
        enquadramentos_data = validated_data.pop('enquadramentos', [])

        # Gera número CRR se não fornecido
        if not validated_data.get('numeroCrr'):
            validated_data['numeroCrr'] = gerar_numero_crr_mobile()

        # Cria veículo (primeira entrada da lista)
        if veiculo_data:
            # Pega o primeiro veículo da lista
            primeiro_veiculo = veiculo_data[0]
            veiculo = Veiculo.objects.create(**primeiro_veiculo)
            validated_data['veiculo'] = veiculo
        else:
            # Se nenhum veículo for fornecido
            raise serializers.ValidationError("Pelo menos um veículo é obrigatório")

        # Cria CRR
        crr = Crr.objects.create(**validated_data)

        # Cria condutores
        for condutor in condutores_data:
            Condutor.objects.create(crr=crr, **condutor)

        # Cria AITs
        for ait in aits_data:
            Ait.objects.create(crr=crr, **ait)

        # Cria enquadramentos
        for enquadramento in enquadramentos_data:
            Enquadramento.objects.create(crr=crr, **enquadramento)

        return crr

    def update(self, instance, validated_data):
        # Lógica similar ao create, mas para atualização
        veiculo_data = validated_data.pop('veiculo', [])
        condutores_data = validated_data.pop('condutores', [])
        aits_data = validated_data.pop('aits', [])
        enquadramentos_data = validated_data.pop('enquadramentos', [])

        # Atualiza atributos do CRR
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualiza veículo
        if veiculo_data:
            primeiro_veiculo = veiculo_data[0]
            veiculo = instance.veiculo
            for attr, value in primeiro_veiculo.items():
                setattr(veiculo, attr, value)
            veiculo.save()

        # Atualiza relacionamentos
        instance.condutores.all().delete()
        for condutor in condutores_data:
            Condutor.objects.create(crr=instance, **condutor)

        instance.aits.all().delete()
        for ait in aits_data:
            Ait.objects.create(crr=instance, **ait)

        instance.enquadramentos.all().delete()
        for enquadramento in enquadramentos_data:
            Enquadramento.objects.create(crr=instance, **enquadramento)

        return instance
def gerar_numero_crr_mobile():
    prefixo = "E-"
    ultimo_crr = Crr.objects.filter(numeroCrr__startswith=prefixo).order_by('-numeroCrr').first()
    if ultimo_crr and ultimo_crr.numeroCrr:
        try:
            ultimo_num = int(ultimo_crr.numeroCrr.replace(prefixo, ""))
        except ValueError:
            ultimo_num = 0
    else:
        ultimo_num = 0
    proximo_num = ultimo_num + 1
    return f"{prefixo}{str(proximo_num).zfill(2)}"