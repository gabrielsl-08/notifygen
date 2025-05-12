from docx import Document
from docx.shared import Inches
from django.http import HttpResponse
from io import BytesIO
from django.utils.timezone import now
from datetime import datetime
import locale
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn
from notificacao.models import NumeroEdital

def obter_proximo_numero_edital():
    obj, _ = NumeroEdital.objects.get_or_create(id=1)
    return obj
    

def gerar_edital_docx(crrs):

    
    
    #arrendatario = crrs.arrendatario
    doc = Document()
    # Carrega o template existente
    doc = Document('media/modelo_edital.docx')
    # Substitui o placeholder {{DATA_ATUAL}} pela data atual formatada
    numero_edital_obj = obter_proximo_numero_edital()
    numero_edital = str(numero_edital_obj.numero)
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/Mac
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'pt_BR') 
    data_formatada = now().strftime('%d DE %B DE %Y').upper()
    
    for paragraph in doc.paragraphs:
        if "{{DATA_ATUAL}}" in paragraph.text or "{{NUMERO_EDITAL}}" in paragraph.text:
            for run in paragraph.runs:
                if "{{DATA_ATUAL}}" in run.text:
                    run.text = run.text.replace("{{DATA_ATUAL}}", data_formatada)
                    run.font.name = 'Verdana'
                    run.font.size = Pt(11)
                    run.bold = True
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Verdana')
                if "{{NUMERO_EDITAL}}" in run.text:
                    run.text = run.text.replace("{{NUMERO_EDITAL}}", numero_edital)
                    run.font.name = 'Verdana'
                    run.font.size = Pt(11)
                    run.bold = True
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
   

    # Adiciona a tabela no final
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'  # Deixa as bordas visíveis

    # Define cabeçalho
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'PLACA/CHASSI'
    hdr_cells[1].text = 'MARCA/MODELO'
    hdr_cells[2].text = 'RESPONSÁVEL'
    hdr_cells[3].text = 'AGENTE FINACEIRO/ARRENDATÁRIO'

    # Exemplo de adição de linha — você pode depois popular com seu queryset
    for crr in crrs:
        row_cells = table.add_row().cells 
        
        row_cells[0].text = str(crr.placa_chassi).upper()
        row_cells[1].text = str(f"{crr.marca}/{crr.modelo}").upper() 
        destinatario = getattr(crr.notificacao, 'destinatario', '') if hasattr(crr, 'notificacao') else ''
        row_cells[2].text = destinatario.upper()
        arrendatario_obj = crr.arrendatarios.first()
        nome_arrendatario = getattr(arrendatario_obj.arrendatario, 'nome_arrendatario', '') if arrendatario_obj and hasattr(arrendatario_obj, 'arrendatario') else ''
        row_cells[3].text = nome_arrendatario.upper()

        

    # Salvar o arquivo em memória
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Criar resposta para download
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="edital_{now().strftime("%Y%m%d_%H%M%S")}.docx"'
    
    numero_edital_obj.incrementar()

    return response

