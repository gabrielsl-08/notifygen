# serializers.py
from rest_framework import serializers
from .models import (Crr,Veiculo ,Condutor,Ait, Enquadramento,TabelaEnquadramento)




class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        exclude = ['crr']

class CondutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condutor
        exclude = ['crr']

class AitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ait
        exclude = ['crr']

class EnquadramentoSerializer(serializers.ModelSerializer):
    enquadramento = serializers.SlugRelatedField(
        slug_field='codigo',
        queryset=TabelaEnquadramento.objects.all()
    )
    class Meta:
        model = Enquadramento
        exclude = ['crr']
'''
class AgenteAutuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenteAutuador
        fields = '__all__'
'''

class TabelaEnquadramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaEnquadramento
        fields = '__all__'


class CrrSerializer(serializers.ModelSerializer):
    # Captura os campos relacionados de forma achatada (flat)
    placa = serializers.CharField(write_only=True)
    chassi = serializers.CharField(write_only=True)
    marca = serializers.CharField(write_only=True)
    modelo = serializers.CharField(write_only=True)
    cor = serializers.CharField(write_only=True)
    

    nomeCondutor = serializers.CharField(write_only=True)
    cpfCondutor = serializers.CharField(write_only=True)
    cnh = serializers.CharField(write_only=True)
    cnhEstrangeira = serializers.CharField(write_only=True)
    

    aits = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    enquadramentos = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Crr
        fields = [
            # Campos do modelo Crr
            'localFiscalizacao', 'municipioEstadoFiscalizacao', 'dataFiscalizacao',
            'horaFiscalizacao', 'medidaAdministrativa', 'localPatio', 'placaGuincho',
            'encarregado', 'observacao', 'matriculaAgente',
            # Campos virtuais relacionados
            'placa', 'chassi', 'marca', 'modelo', 'cor', 
            'nomeCondutor', 'cpfCondutor', 'cnh', 'cnhEstrangeira', 
            'aits', 'enquadramentos'
        ]

    def create(self, validated_data):
        # Extrai dados relacionados
        veiculo_data = {
            'placa': validated_data.pop('placa'),
            'chassi': validated_data.pop('chassi'),
            'marca': validated_data.pop('marca'),
            'modelo': validated_data.pop('modelo'),
            'cor': validated_data.pop('cor'),
        }
        condutor_data = {
            'nomeCondutor': validated_data.pop('nomeCondutor'),
            'cpfCondutor': validated_data.pop('cpfCondutor'),
            'cnh': validated_data.pop('cnh'),
            'cnhEstrangeira': validated_data.pop('cnhEstrangeira'),
        }

        aits_list = validated_data.pop('aits', [])
        enquadramentos_list = validated_data.pop('enquadramentos', [])

        try:
            # Cria o CRR primeiro (sem veiculo e condutor ainda)
            crr = Crr.objects.create(**validated_data)

            # Agora sim, cria veiculo e condutor com crr associado
            veiculo = Veiculo.objects.create(crr=crr, **veiculo_data)
            condutor = Condutor.objects.create(crr=crr, **condutor_data)

            # Atualiza CRR com os relacionamentos
            crr.veiculo = veiculo
            crr.condutor = condutor
            crr.save()

            # Cria AITs associados
            for numero_ait in aits_list:
                Ait.objects.create(crr=crr, ait=numero_ait)

            # Cria Enquadramentos associados
            for codigo in enquadramentos_list:
                codigo_str = str(codigo).zfill(5)
                if not codigo_str.isdigit() or len(codigo_str) != 5:
                    raise serializers.ValidationError(
                        f"Código de enquadramento inválido: '{codigo_str}'. Deve conter 5 dígitos numéricos."
                    )
                enquad_obj, _ = TabelaEnquadramento.objects.get_or_create(
                    codigo=codigo_str,
                    defaults={
                        "amparo_legal": "NÃO INFORMADO",
                        "descricao_infracao": "ENQUADRAMENTO CADASTRADO AUTOMATICAMENTE"
                    }
                )
                Enquadramento.objects.create(crr=crr, enquadramento=enquad_obj)

            return crr

        except Exception as e:
            print(f"[ERRO CRR] {e}")
            raise serializers.ValidationError(f"Erro ao criar CRR: {e}")

    def validate(self, data):
        # Campos obrigatórios customizados
        campos = ['placa', 'marca', 'nomeCondutor', 'cpfCondutor', 'dataFiscalizacao', 'horaFiscalizacao']
        for campo in campos:
            if not data.get(campo):
                raise serializers.ValidationError(f"O campo '{campo}' é obrigatório.")
        return data

   

        