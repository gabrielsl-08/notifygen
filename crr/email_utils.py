import os
import smtplib
from django.core.mail import EmailMessage
from django.conf import settings


def _wrap_email(label, valor, largura=60):
    """Formata 'label: VALOR' com quebra de linha para email."""
    prefixo = f"{label}: "
    valor = str(valor).upper()
    disp = largura - len(prefixo)
    if disp <= 4 or len(valor) <= disp:
        return [prefixo + valor]
    linhas = []
    cont = " " * len(prefixo)
    linhas.append(prefixo + valor[:disp])
    resto = valor[disp:]
    while resto:
        linhas.append(cont + resto[:largura - len(cont)])
        resto = resto[largura - len(cont):]
    return linhas


def gerar_texto_crr(crr):
    """Gera texto formatado do CRR para anexo de email.
    Layout identico ao impresso, com largura adaptada para email."""
    LARG = 60
    DIV = "-" * LARG
    linhas = []

    data = crr.dataFiscalizacao.strftime('%d/%m/%Y') if crr.dataFiscalizacao else '-'
    hora = crr.horaFiscalizacao.strftime('%H:%M') if crr.horaFiscalizacao else '-'

    # Titulo
    linhas.append("COMPROVANTE DE RECOLHIMENTO E REMOCAO - CRR")

    # Identificacao
    linhas.append(DIV)
    linhas.append("IDENTIFICACAO DO CRR")
    linhas.append(DIV)
    linhas += _wrap_email("numero", crr.numeroCrr, LARG)
    linhas += _wrap_email("data", data, LARG)
    linhas += _wrap_email("hora", hora, LARG)

    # Veiculo
    linhas.append(DIV)
    linhas.append("VEICULO")
    linhas.append(DIV)
    v = crr.veiculo.first()
    linhas += _wrap_email("placa", v.placa if v and v.placa else '-', LARG)
    linhas += _wrap_email("chassi", v.chassi if v and v.chassi else '-', LARG)
    linhas += _wrap_email("marca", v.marca if v and v.marca else '-', LARG)
    linhas += _wrap_email("modelo", v.modelo if v and v.modelo else '-', LARG)
    linhas += _wrap_email("cor", v.cor if v and v.cor else '-', LARG)

    # Fiscalizacao
    linhas.append(DIV)
    linhas.append("FISCALIZACAO")
    linhas.append(DIV)
    linhas += _wrap_email("local", crr.localFiscalizacao or '-', LARG)
    linhas += _wrap_email("medida", crr.medidaAdministrativa or '-', LARG)

    aits = [a.ait for a in crr.aits.all()]
    if aits:
        linhas += _wrap_email("AITs", ', '.join(a.upper() for a in aits), LARG)

    enqs = [
        str(e.enquadramento.codigo)
        for e in crr.enquadramentos.all()
        if e.enquadramento
    ]
    if enqs:
        linhas += _wrap_email("enquadr.", ', '.join(enqs), LARG)
        if '00000' in enqs:
            linhas.append("  ART. 279-A")

    # Outros dados
    linhas.append(DIV)
    linhas.append("OUTROS DADOS")
    linhas.append(DIV)
    linhas += _wrap_email("patio", crr.localPatio or '-', LARG)
    linhas += _wrap_email("guincho", crr.placaGuincho or '-', LARG)
    linhas += _wrap_email("encarr.", crr.encarregado or '-', LARG)
    linhas += _wrap_email("agente", crr.matriculaAgente or '-', LARG)

    # Condutor
    linhas.append(DIV)
    linhas.append("CONDUTOR")
    linhas.append(DIV)
    c = crr.condutores.first()
    if c and c.nomeCondutor:
        linhas += _wrap_email("nome", c.nomeCondutor, LARG)
        linhas += _wrap_email("cpf", c.cpfCondutor or '-', LARG)
    else:
        linhas.append("ausente")

    # Observacao
    if crr.observacao:
        linhas.append(DIV)
        linhas.append("OBSERVACAO")
        linhas.append(DIV)
        linhas += _wrap_email("obs.", crr.observacao, LARG)

    # Assinatura condutor
    linhas.append(DIV)
    linhas.append("")
    linhas.append("assinatura do condutor:")
    linhas.append("_" * LARG)

    situacao = crr.situacaoEntrega or ''
    if situacao:
        linhas.append(situacao.upper())

    linhas.append(DIV)
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


def enviar_email_condutor(crr, email_condutor):
    """
    Envia email ao condutor com o CRR como anexo .txt.
    Retorna (True, '') em sucesso, (False, 'mensagem') em falha.
    """
    if not email_condutor:
        return False, 'Email do condutor não informado'

    try:
        v = crr.veiculo.first()
        placa = v.placa.upper() if v and v.placa else 'S/PLACA'
        data = (
            crr.dataFiscalizacao.strftime('%d/%m/%Y')
            if crr.dataFiscalizacao else '-'
        )
        assunto = f"CRR {crr.numeroCrr.upper()} — {placa} — {data}"
        corpo = (
            f"Prezado(a),\n\n"
            f"Segue em anexo o Comprovante de Recolhimento e Remoção "
            f"(CRR) nº {crr.numeroCrr.upper()}, referente ao veículo "
            f"de placa {placa}, lavrado em {data}.\n\n"
            f"Atenciosamente,\n"
            f"Fiscalização de Trânsito"
        )
        texto = gerar_texto_crr(crr)
        nome_arquivo = f"crr_{crr.numeroCrr}.txt"

        email = EmailMessage(
            subject=assunto,
            body=corpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_condutor],
        )
        email.attach(nome_arquivo, texto, 'text/plain')
        connection = email.get_connection()
        connection.timeout = 20
        email.connection = connection
        email.send(fail_silently=False)
        return True, ''

    except smtplib.SMTPException as e:
        return False, f'Erro SMTP: {str(e)}'
    except Exception as e:
        return False, str(e)
