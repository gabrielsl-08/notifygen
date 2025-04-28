from crr.models import Crr

def gerar_proximo_numero_crr():
    # Buscar todos que começam com "E-"
    ultimos_crrs = Crr.objects.filter(numero_crr__startswith="E-").order_by('-numero_crr')

    if not ultimos_crrs.exists():
        return "E-01"

    ultimo_numero = ultimos_crrs.first().numero_crr  # Exemplo: "E-07"
    try:
        ultimo_numero_int = int(ultimo_numero.split('-')[1])
    except (IndexError, ValueError):
        ultimo_numero_int = 0

    novo_numero = ultimo_numero_int + 1
    return f"E-{novo_numero:02d}"  # sempre 2 dígitos