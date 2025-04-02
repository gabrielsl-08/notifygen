from django import forms

class AmparoLegalWidget(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'list': 'amparoLegalOptions'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        opcoes = [
            "Art. 279-A C.T.B.",
            "Art. 230, V - C.T.B.",
            "Lei 9.503/97"
        ]
        html += f"""
        <datalist id="amparoLegalOptions">
            {''.join(f'<option value="{opcao}">' for opcao in opcoes)}
        </datalist>
        """
        return html