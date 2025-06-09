# crr/forms.py
from django import forms
from .models import Crr,Veiculo,Condutor,Ait, Enquadramento,ImagemCrr 

class CrrForm(forms.ModelForm):
    class Meta:
        model = Crr
        fields = ['numeroCrr','matriculaAgente','placaGuincho', 'encarregado',
                  'localFiscalizacao', 'dataFiscalizacao','horaFiscalizacao','observacao'
                  ]

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','chassi','marca', 'modelo', 'cor','especie',
                  'categoria','ufVeiculo','municipioVeiculo']


class CondutorForm(forms.ModelForm):
    class Meta:
        model = Condutor
        fields = ['nomeCondutor','cnh','cnhEstrangeira', 'ufCnh', 'cpfCondutor']

class AitForm(forms.ModelForm):
    class Meta:
        model = Ait
        fields = ['ait']

class EnquadramentoForm(forms.ModelForm):
    class Meta:
        model = Enquadramento
        fields = ['enquadramento']

class ImagemCrrForm(forms.ModelForm):
    class Meta:
        model = ImagemCrr
        fields = ['imagem']