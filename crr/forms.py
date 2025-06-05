# crr/forms.py
from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Crr,Veiculo,Condutor,Ait, Enquadramento,ImagemCrr 

class CrrForm(ModelForm):
    class Meta:
        model = Crr
        fields = [
           'status' , 'numeroCrr','matriculaAgente', 'dataFiscalizacao', 
            'horaFiscalizacao','localFiscalizacao', 'observacao', 
             'placaGuincho', 'encarregado'
            
        ]

class VeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','chassi','marca','modelo','cor','especie',
                  'categoria','ufVeiculo','municipioVeiculo']

# Formset para AITs aninhados em CRR
VeiculoFormSet = inlineformset_factory(Crr,Veiculo,form=VeiculoForm,extra=1,can_delete=True)

class CondutorForm(ModelForm):
    class Meta:
        model = Condutor
        fields = ['cnh','cnhEstrangeira', 'ufCnh', 'cpfCondutor','nomeCondutor',]

# Formset para AITs aninhados em CRR
CondutorFormSet = inlineformset_factory(Crr,Condutor,form=CondutorForm,extra=1,can_delete=True)

class AitForm(ModelForm):
    class Meta:
        model = Ait
        fields = ['ait',]

# Formset para AITs aninhados em CRR
AitFormSet = inlineformset_factory(Crr,Ait,form=AitForm,extra=4, max_num=4,can_delete=True)

class EnquadramentoForm(ModelForm):
    class Meta:
        model = Enquadramento
        fields = ['enquadramento',]

# Formset para AITs aninhados em CRR
EnquadramentoFormSet = inlineformset_factory(Crr,Enquadramento,form=EnquadramentoForm,extra=1, max_num=4,can_delete=True)

class ImagemCrrForm(ModelForm):
    class Meta:
        model = ImagemCrr
        fields = ['imagem',]

# Formset para AITs aninhados em CRR
ImagemCrrFormSet = inlineformset_factory(Crr,ImagemCrr,form=ImagemCrrForm,extra=1, max_num=4,can_delete=True)