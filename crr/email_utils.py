import os
from django.core.mail import EmailMessage
from django.conf import settings


def gerar_texto_crr(crr):
    """Gera texto formatado do CRR para anexo de email."""
    SEP = "=" * 40
    DIV = "-" * 40
    linhas = []

    linhas.append(SEP)
    linhas.append("COMPROVANTE DE RECOLHIMENTO E REMOCAO")
    linhas.append(SEP)
    linhas.append(f"NUMERO: {crr.numeroCrr.upper()}")
    data = crr.dataFiscalizacao.strftime('%d/%m/%Y') if crr.dataFiscalizacao else '-'
    hora = crr.horaFiscalizacao.strftime('%H:%M') if crr.horaFiscalizacao else '-'
    linhas.append(f"DATA: {data}")
    linhas.append(f"HORA: {hora}")
    linhas.append(f"STATUS: {crr.get_status_display().upper()}")
    linhas.append(DIV)

    v = crr.veiculo.first()
    if v:
        linhas.append("VEICULO:")
        linhas.append(f"  PLACA:  {v.placa.upper() if v.placa else '-'}")
        linhas.append(f"  CHASSI: {v.chassi.upper() if v.chassi else '-'}")
        linhas.append(f"  MARCA:  {v.marca.upper() if v.marca else '-'}")
        linhas.append(f"  MODELO: {v.modelo.upper() if v.modelo else '-'}")
        linhas.append(f"  COR:    {v.cor.upper() if v.cor else '-'}")
    linhas.append(DIV)

    linhas.append("FISCALIZACAO:")
    local = crr.localFiscalizacao.upper() if crr.localFiscalizacao else '-'
    medida = crr.medidaAdministrativa.upper() if crr.medidaAdministrativa else '-'
    linhas.append(f"  LOCAL:  {local}")
    linhas.append(f"  MEDIDA: {medida}")
    linhas.append(DIV)

    aits = [a.ait for a in crr.aits.all()]
    if aits:
        linhas.append(f"  AITs: {', '.join(a.upper() for a in aits)}")

    enqs = [
        str(e.enquadramento.codigo)
        for e in crr.enquadramentos.all()
        if e.enquadramento
    ]
    if enqs:
        linhas.append(f"  ENQUADR.: {', '.join(enqs)}")
    linhas.append(DIV)

    linhas.append("OUTROS DADOS:")
    linhas.append(f"  PATIO:       {crr.localPatio.upper() if crr.localPatio else '-'}")
    linhas.append(f"  GUINCHO:     {crr.placaGuincho.upper() if crr.placaGuincho else '-'}")
    linhas.append(f"  ENCARREGADO: {crr.encarregado.upper() if crr.encarregado else '-'}")
    linhas.append(f"  AGENTE:      {crr.matriculaAgente.upper() if crr.matriculaAgente else '-'}")
    linhas.append(DIV)

    c = crr.condutores.first()
    linhas.append("CONDUTOR:")
    if c and c.nomeCondutor:
        linhas.append(f"  NOME: {c.nomeCondutor.upper()}")
        linhas.append(f"  CPF:  {c.cpfCondutor or '-'}")
        linhas.append(f"  CNH:  {c.cnh or '-'}")
    else:
        linhas.append("  AUSENTE")

    if crr.observacao:
        linhas.append(DIV)
        linhas.append(f"OBS: {crr.observacao.upper()}")

    linhas.append(SEP)
    return "\n".join(linhas)


def enviar_email_crr(crr):
    """
    Envia email ao pátio com o CRR como anexo .txt.
    Retorna True em sucesso, False em falha.
    Nunca lança exceção — falha silenciosa para não bloquear a API.
    """
    destino = os.environ.get('EMAIL_PATIO_DESTINO', '')
    if not destino:
        return False

    try:
        v = crr.veiculo.first()
        placa = v.placa.upper() if v and v.placa else 'S/PLACA'
        data = (
            crr.dataFiscalizacao.strftime('%d/%m/%Y')
            if crr.dataFiscalizacao else '-'
        )
        assunto = f"CRR {crr.numeroCrr.upper()} — {placa} — {data}"
        corpo = (
            f"Segue em anexo o CRR {crr.numeroCrr.upper()} "
            f"registrado pelo agente de fiscalização."
        )
        texto = gerar_texto_crr(crr)
        nome_arquivo = f"crr_{crr.numeroCrr}.txt"

        email = EmailMessage(
            subject=assunto,
            body=corpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destino],
        )
        email.attach(nome_arquivo, texto, 'text/plain')
        email.send(fail_silently=False)
        return True

    except Exception:
        return False
