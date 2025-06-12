# crr/forms.py
from django import forms
from .models import Crr,Veiculo,Condutor,Ait, Enquadramento,ImagemCrr 
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

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

class CrrForm(ModelForm):
    class Meta:
        model = Crr
        fields = '__all__'

VeiculoFormSet = inlineformset_factory(Crr, Veiculo, fields='__all__', extra=0, can_delete=False)
CondutorFormSet = inlineformset_factory(Crr, Condutor, fields='__all__', extra=0, can_delete=False)
AitFormSet = inlineformset_factory(Crr, Ait, fields='__all__', extra=0, can_delete=False)
EnquadramentoFormSet = inlineformset_factory(Crr, Enquadramento, fields='__all__', extra=0, can_delete=False)
ImagemCrrFormSet = inlineformset_factory(Crr, ImagemCrr, fields='__all__', extra=0, can_delete=False)