from docx import Document
from docx.shared import Inches
from django.http import HttpResponse
from io import BytesIO
from django.utils.timezone import now

def gerar_edital_docx(crrs):
    doc = Document()
    # Carrega o template existente
    doc = Document('C:/Users/gabriel/Desktop/divprom/media/modelo_edital.docx')

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
        row_cells[0].text = str(crr.placa_chassi)
        row_cells[1].text = str(f"{crr.marca}/{crr.modelo}")  
        row_cells[2].text = str(crr.cpf)
        row_cells[3].text = str(crr.arrendatario)

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
    return response

