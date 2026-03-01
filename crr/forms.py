from django import forms
from django.forms import inlineformset_factory
from .models import Crr, Condutor, Veiculo, Ait, Enquadramento, Arrendatario, ImagemCrr, TabelaEnquadramento, TabelaArrendatario


class CrrForm(forms.ModelForm):
    class Meta:
        model = Crr
        fields = [
            'numeroCrr', 'localFiscalizacao', 'dataFiscalizacao',
            'horaFiscalizacao', 'placaGuincho', 'encarregado',
            'observacao', 'matriculaAgente'
        ]
        widgets = {
            'numeroCrr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do CRR'}),
            'localFiscalizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local da Fiscalização'}),
            'dataFiscalizacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'horaFiscalizacao': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'placaGuincho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa do Guincho'}),
            'encarregado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Encarregado'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações'}),
            'matriculaAgente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula do Agente'}),
        }


class CondutorForm(forms.ModelForm):
    class Meta:
        model = Condutor
        fields = ['nomeCondutor', 'cpfCondutor', 'cnh', 'cnhEstrangeira', 'ufCnh']
        widgets = {
            'nomeCondutor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Condutor'}),
            'cpfCondutor': forms.TextInput(attrs={'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'}),
            'cnh': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNH'}),
            'cnhEstrangeira': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNH Estrangeira'}),
            'ufCnh': forms.Select(attrs={'class': 'form-select'}),
        }


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'chassi', 'marca', 'modelo', 'cor', 'especie', 'categoria', 'ufVeiculo', 'municipioVeiculo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control placa-mask', 'placeholder': 'ABC1234'}),
            'chassi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chassi'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cor'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'ufVeiculo': forms.Select(attrs={'class': 'form-select'}),
            'municipioVeiculo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Município'}),
        }


class AitForm(forms.ModelForm):
    class Meta:
        model = Ait
        fields = ['ait']
        widgets = {
            'ait': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código AIT'}),
        }


class EnquadramentoForm(forms.ModelForm):
    class Meta:
        model = Enquadramento
        fields = ['enquadramento']
        widgets = {
            'enquadramento': forms.Select(attrs={'class': 'form-select'}),
        }


class ArrendatarioForm(forms.ModelForm):
    class Meta:
        model = Arrendatario
        fields = ['arrendatario']
        widgets = {
            'arrendatario': forms.Select(attrs={'class': 'form-select'}),
        }


class ImagemCrrForm(forms.ModelForm):
    class Meta:
        model = ImagemCrr
        fields = ['imagem']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class TabelaArrendatarioForm(forms.ModelForm):
    class Meta:
        model = TabelaArrendatario
        fields = [
            'nome_arrendatario', 'cnpj_arrendatario', 'endereco_arrendatario',
            'numero_arrendatario', 'complemento_arrendatario', 'bairro_arrendatario',
            'cidade_arrendatario', 'uf_arrendatario', 'cep_arrendatario',
        ]
        widgets = {
            'nome_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj_arrendatario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0001-00'}),
            'endereco_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade_arrendatario': forms.TextInput(attrs={'class': 'form-control'}),
            'uf_arrendatario': forms.Select(attrs={'class': 'form-select'}),
            'cep_arrendatario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
        }


class TabelaEnquadramentoForm(forms.ModelForm):
    class Meta:
        model = TabelaEnquadramento
        fields = ['codigo', 'amparo_legal', 'descricao_infracao']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 51930'}),
            'amparo_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_infracao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Formsets para os modelos relacionados
CondutorFormSet = inlineformset_factory(
    Crr, Condutor, form=CondutorForm,
    extra=1, max_num=1, can_delete=True
)

VeiculoFormSet = inlineformset_factory(
    Crr, Veiculo, form=VeiculoForm,
    extra=1, max_num=1, can_delete=True
)

AitFormSet = inlineformset_factory(
    Crr, Ait, form=AitForm,
    extra=1, max_num=4, can_delete=True
)

EnquadramentoFormSet = inlineformset_factory(
    Crr, Enquadramento, form=EnquadramentoForm,
    extra=1, max_num=4, can_delete=True
)

ArrendatarioFormSet = inlineformset_factory(
    Crr, Arrendatario, form=ArrendatarioForm,
    extra=1, max_num=1, can_delete=True
)

ImagemCrrFormSet = inlineformset_factory(
    Crr, ImagemCrr, form=ImagemCrrForm,
    extra=1, max_num=4, can_delete=True
)
