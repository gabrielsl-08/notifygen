from docx import Document
from docx.shared import Inches
from django.http import HttpResponse
from io import BytesIO
from django.utils.timezone import now

def gerar_edital_docx(crrs):
    document = Document()

    # Título
    document.add_heading('EDITAL DE NOTIFICAÇÃO', level=1)
    document.add_paragraph(f'Data de emissão: {now().date()}')
    document.add_paragraph('Lista de veículos retidos há mais de 30 dias:')

    # Tabela com os dados
    table = document.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'ID'
    hdr_cells[1].text = 'Data de Remoção'
    hdr_cells[2].text = 'Status'

    for crr in crrs:
        row_cells = table.add_row().cells
        row_cells[0].text = str(crr.id)
        row_cells[1].text = str(crr.data_remocao)
        row_cells[2].text = crr.status

    # Salvar o arquivo em memória
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Criar resposta para download
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="edital_{now().strftime("%Y%m%d_%H%M%S")}.docx"'
    return response
