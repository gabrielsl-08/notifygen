from django import forms
from crr.models import Crr, Ait, TabelaEnquadramento
from .utils import gerar_proximo_numero_crr

class CrrForm(forms.ModelForm):
    ait = forms.CharField(
        label='Código de AIT', 
        max_length=11, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    enquadramento = forms.ModelChoiceField(
        queryset=TabelaEnquadramento.objects.all(),
        label="Enquadramento",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Crr
        fields = [
            'placa_chassi', 'marca', 'modelo', 'especie', 'categoria', 'uf_veiculo', 'municipio_veiculo',
            'local_remocao', 'data_remocao', 'hora_remocao', 'observacao',
            'nome_condutor', 'habilitacao_condutor', 'uf_cnh', 'cpf',
        ]
        widgets = {
            'data_remocao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_remocao': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'placa_chassi': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'uf_veiculo': forms.Select(attrs={'class': 'form-select'}),
            'municipio_veiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'local_remocao': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'nome_condutor': forms.TextInput(attrs={'class': 'form-control'}),
            'habilitacao_condutor': forms.TextInput(attrs={'class': 'form-control'}),
            'uf_cnh': forms.Select(attrs={'class': 'form-select'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        }
