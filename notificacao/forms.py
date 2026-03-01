from django import forms
from .models import Notificacao
from crr.models import Crr


class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = [
            'crr', 'data_emissao', 'data_postagem',
            'destinatario', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade_destinatario', 'uf_destinatario', 'cep',
        ]
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_postagem': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'crr': forms.Select(attrs={'class': 'form-select'}),
            'uf_destinatario': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas CRRs com status retido podem ser notificados
        self.fields['crr'].queryset = Crr.objects.filter(status='retido').order_by('numeroCrr')
        for name, field in self.fields.items():
            if name not in ('crr', 'uf_destinatario', 'data_emissao', 'data_postagem'):
                field.widget.attrs.setdefault('class', 'form-control')
