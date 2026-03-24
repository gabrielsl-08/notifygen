import os
import smtplib
from django.core.mail import EmailMessage
from django.conf import settings


def gerar_texto_crr(crr):
    """Gera texto formatado do CRR para anexo de email.
    Layout identico ao impresso (print_utils.py)."""
    DIV = "-" * 32
    linhas = []

    data = crr.dataFiscalizacao.strftime('%d/%m/%Y') if crr.dataFiscalizacao else '-'
    hora = crr.horaFiscalizacao.strftime('%H:%M') if crr.horaFiscalizacao else '-'

    # Titulo
    linhas.append("COMPROVANTE DE RECOLHIMENTO")
    linhas.append("E REMOCAO - CRR")

    # Identificacao
    linhas.append(DIV)
    linhas.append("IDENTIFICACAO DO CRR")
    linhas.append(DIV)
    linhas.append(f"numero: {crr.numeroCrr.upper()}")
    linhas.append(f"data: {data}")
    linhas.append(f"hora: {hora}")

    # Veiculo
    linhas.append(DIV)
    linhas.append("VEICULO")
    linhas.append(DIV)
    v = crr.veiculo.first()
    linhas.append(f"placa: {v.placa.upper() if v and v.placa else '-'}")
    linhas.append(f"chassi: {v.chassi.upper() if v and v.chassi else '-'}")
    linhas.append(f"marca: {v.marca.upper() if v and v.marca else '-'}")
    linhas.append(f"modelo: {v.modelo.upper() if v and v.modelo else '-'}")
    linhas.append(f"cor: {v.cor.upper() if v and v.cor else '-'}")

    # Fiscalizacao
    linhas.append(DIV)
    linhas.append("FISCALIZACAO")
    linhas.append(DIV)
    linhas.append(f"local: {crr.localFiscalizacao.upper() if crr.localFiscalizacao else '-'}")
    linhas.append(f"medida: {crr.medidaAdministrativa.upper() if crr.medidaAdministrativa else '-'}")

    aits = [a.ait for a in crr.aits.all()]
    if aits:
        linhas.append(f"AITs: {', '.join(a.upper() for a in aits)}")

    enqs = [
        str(e.enquadramento.codigo)
        for e in crr.enquadramentos.all()
        if e.enquadramento
    ]
    if enqs:
        linhas.append(f"enquadr.: {', '.join(enqs)}")
        if '00000' in enqs:
            linhas.append("  ART. 279-A")

    # Outros dados
    linhas.append(DIV)
    linhas.append("OUTROS DADOS")
    linhas.append(DIV)
    linhas.append(f"patio: {crr.localPatio.upper() if crr.localPatio else '-'}")
    linhas.append(f"guincho: {crr.placaGuincho.upper() if crr.placaGuincho else '-'}")
    linhas.append(f"encarr.: {crr.encarregado.upper() if crr.encarregado else '-'}")
    linhas.append(f"agente: {crr.matriculaAgente.upper() if crr.matriculaAgente else '-'}")

    # Condutor
    linhas.append(DIV)
    linhas.append("CONDUTOR")
    linhas.append(DIV)
    c = crr.condutores.first()
    if c and c.nomeCondutor:
        linhas.append(f"nome: {c.nomeCondutor.upper()}")
        linhas.append(f"cpf: {c.cpfCondutor or '-'}")
    else:
        linhas.append("ausente")

    # Observacao
    if crr.observacao:
        linhas.append(DIV)
        linhas.append("OBSERVACAO")
        linhas.append(DIV)
        linhas.append(f"obs.: {crr.observacao.upper()}")

    # Assinatura condutor
    linhas.append(DIV)
    linhas.append("")
    linhas.append("assinatura do condutor:")
    linhas.append("_" * 32)

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
