from django import forms

from .questoes import QUESTOES


class QuestionarioForm(forms.Form):
    nome_completo = forms.CharField(
        label='Nome completo',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seuemail@exemplo.com'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for questao in QUESTOES:
            choices = [(letra, texto) for letra, texto in questao['alternativas'].items()]
            self.fields[f'questao_{questao["id"]}'] = forms.ChoiceField(
                label=questao['enunciado'],
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
            )
        self.fields['criticas_sugestoes'] = forms.CharField(
            label='Críticas, sugestões de temas para discussão, etc.',
            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            required=False,
        )

    def campos_questoes(self):
        """Retorna lista de (questao, campo_do_form) para uso no template."""
        return [(questao, self[f'questao_{questao["id"]}']) for questao in QUESTOES]
