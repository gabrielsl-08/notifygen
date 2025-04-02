from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import LETTER,A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph


def render_notificacao_template(c, notificacao, width, height):
    largura, altura = LETTER 


  # Alterado para LETTER (Carta)




    
    # Registrar fonte personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c.setFont("Arial", 10)
    
    # Título principal
   
    c.drawString(7 * cm, altura - 4.5 * cm, "PREFEITURA MUNICIPAL DE SÃO SEBASTIÃO")

    c.setFont("Arial", 8)
    c.drawString(7 * cm, altura - 4.9 * cm, "SECRETARIA DE SEGURANÇA URBANA")

     
    c.line(2 * cm, altura - 5.0 * cm, largura - 2 * cm, altura - 5.0 * cm)

    c.setFont("Arial", 10)
    c.drawString(5 * cm, altura - 5.4 * cm, "NOTIFICAÇÃO DE AUTUAÇÃO POR INFRAÇÃO A LEI 2771/2020")
    
    # Linha horizontal abaixo de notificação de autuação por infração de trânsito
    c.line(2 * cm, altura - 5.5 * cm, largura - 2 * cm, altura - 5.5 * cm)
    
    # Identificação da Autuação
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 5.9 * cm, "Identificação da Autuação")
    # 1ª Linha horizontal abaixo de identificação da autuação
    c.line(2 * cm, altura - 6.1 * cm, largura - 2 * cm, altura - 6.1 * cm)
    # 2ª Linha horizontal abaixo de identificação da autuação
    c.line(2 * cm, altura - 7 * cm, largura - 2 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 6.4 * cm, "Código órgão Autuador")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 6.9 * cm,  "271150")
     # Barra vertical
    c.line(5.8* cm, altura - 6.1 * cm, 5.8 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(6 * cm, altura - 6.4 * cm, "Auto de Infração:")
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 6.9 * cm, "T-165")
    # Barra vertical em frente auto de infração
    c.line(9* cm, altura - 6.1 * cm, 9 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(9.5 * cm, altura - 6.4 * cm, "Data da Postagem:")
    c.setFont("Arial", 10)
    c.drawString(9.5 * cm, altura - 6.9 * cm, "05/01/2022")
    # Barra vertical em frente data de postagem
    c.line(12.7* cm, altura - 6.1 * cm, 12.7 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(13 * cm, altura - 6.4 * cm, "Data Emissão:")
    c.setFont("Arial", 10)
    c.drawString(13 * cm, altura - 6.9 * cm, "05/01/2022")
    # Barra vertical em frente data emissão
    c.line(15.7* cm, altura - 6.1 * cm, 15.7 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(16.5 * cm, altura - 6.4 * cm, "Numero Controle:")
    c.setFont("Arial", 10)
    c.drawString(16.5 * cm, altura - 6.9 * cm, "001")
    
    veiculo = notificacao.veiculo
    # Linha horizontal abaixo da identificação do veículo
    c.line(2 * cm, altura - 7.7 * cm, largura - 2 * cm, altura - 7.7 * cm)
    # Identificação do Veículo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 7.5 * cm, "Identificação do Veículo")
    
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 8 * cm, "Placa Veículo:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 8.5 * cm, "EOF7002")

    c.setFont("Arial", 8)
    c.drawString(4.5 * cm, altura - 8 * cm, "Município / UF:")
    c.setFont("Arial", 10)
    c.drawString(4.5 * cm, altura - 8.5 * cm, "SÃO SEBASTIÃO/SP")
    
    c.setFont("Arial", 8)
    c.drawString(8.5 * cm, altura - 8 * cm, "Marca/Modelo:")
    c.setFont("Arial", 10)
    c.drawString(8.5 * cm, altura - 8.5 * cm, f"{veiculo.marca}/{veiculo.modelo}")

    c.setFont("Arial", 8)
    c.drawString(13 * cm, altura - 8 * cm, "Espécie:")
    c.setFont("Arial", 10)
    c.drawString(13 * cm, altura - 8.5 * cm, "PASSAGEIRO")

    c.setFont("Arial", 8)
    c.drawString(17 * cm, altura - 8 * cm, "Categoria:")
    c.setFont("Arial", 10)
    c.drawString(17 * cm, altura - 8.5 * cm, "ALUGUEL")
    
    # Linha horizontal acima de identificação do local da infração
    c.line(2 * cm, altura - 8.6 * cm, largura - 2 * cm, altura - 8.6 * cm)
     # Local da Infração
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10 * cm, altura - 9 * cm, "Identificação do Local da Infração")
        # Linha horizontal abaixo de identificação do local da infração
    c.line(2 * cm, altura - 9.1 * cm, largura - 2 * cm, altura - 9.1 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 9.4 * cm, "Local da Infração")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 9.9 * cm, "AV. MANOEL TEIXEIRA, 425")
        # Linha horizontal abaixo de local da infração
    c.line(2 * cm, altura - 10 * cm, largura - 2 * cm, altura - 10 * cm)

 # Linha horizontal acima de "Município / UF / Código:"
    c.line(2 * cm, altura - 11 * cm, largura - 2 * cm, altura - 11 * cm)
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 11.3* cm, "Município / UF / Código:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 11.7 * cm, "SÃO SEBASTIÃO / SP / 7115")

    c.setFont("Arial", 8)
    c.drawString(7.1 * cm, altura - 11.3 * cm, "Data da Infração:")
    c.setFont("Arial", 10)
    c.drawString(7.1 * cm, altura - 11.7 * cm, "10/12/2021")

    c.setFont("Arial", 8)
    c.drawString(9.7 * cm, altura - 11.3 * cm, "Hora da Infração:")
    c.drawString(9.7 * cm, altura - 11.7 * cm, "10:57")

    # retangulo para imagem
        #   (x  , y,   largura, altura, stroke=1, fill=0)
    c.rect(12*cm, 12.53*cm, 7.5*cm, 4.5*cm , stroke=1, fill=0)

    imagem = notificacao.imagem
    # Imagem Brasão
    try:
        imagem = ImageReader(imagem)  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 12.1 * cm, altura - 15.5 * cm, width=7.5 * cm, height=4.5 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 10.3 * cm, "Observação:")
    c.drawString(2 * cm, altura - 10.8 * cm, "VEÍCULO ABORDADO SEM O DEVIDO CREDENCIAMENTO, "
                                                "NÃO SENDO POSSÍVEL A REDUÇÃO POR FALTA DE MEIOS")
    


    # Linha horizontal acima da tipificação da infração
    c.line(2 * cm, altura - 11.9 * cm, largura - 9.6 * cm, altura - 11.9 * cm)

    # Tipificação da Infração
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.5 * cm, altura - 12.3 * cm, "Tipificação da Infração")
    # Linha horizontal abaixo da tipificação da infração
    c.line(2 * cm, altura - 12.5 * cm, largura - 9.6 * cm, altura - 12.5 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 12.8 * cm, "Descrição da Infração:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 13.5 * cm, "Art. 6 - Lei 2771/2020")

     # Linha horizontal acima de Amparo Legal
    c.line(2 * cm, altura - 14.7 * cm, largura - 9.6 * cm, altura - 14.7 * cm)
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 15 * cm, "Amparo Legal:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 15.4* cm, "Lei 2771/2020")

    c.setFont("Arial", 8)
    c.drawString(6 * cm, altura - 15 * cm, "Identificação da Autoridade/Agente Autuador:")
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 15.4 * cm, "58289")
    
    
    # Linha horizontal acima da identificação de condutor 
    c.line(2 * cm, altura - 15.5 * cm, largura - 2 * cm, altura - 15.5 * cm)
    # Identificação do Condutor
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10 * cm, altura - 15.9 * cm, "Identificação do Condutor")
    # Linha horizontal abaixo de indentificação de condutor
    c.line(2 * cm, altura - 16 * cm, largura - 2 * cm, altura - 16 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 16.3 * cm, "Nº Habilitação do Condutor:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 16.7 * cm, "00601556505")
     #Linha horizontal abaixo da habilitação do condutor
    c.line(2 * cm, altura - 16.8 * cm, largura - 2 * cm, altura - 16.8 * cm)

    c.setFont("Arial", 8)
    c.drawString(6 * cm, altura - 16.3 * cm, "UF:")
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 16.7 * cm, "SP")

    c.setFont("Arial", 8)
    c.drawString(7 * cm, altura - 16.3 * cm, "CPF:")
    c.setFont("Arial", 10)
    c.drawString(7 * cm, altura - 16.7 * cm, "123.456.789-11")
    

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 17.1 * cm, "Nome:")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 17.5 * cm, "EDSON FRANCISCO DA SILVA")
    #Linha horizontal abaixo de NOME
    c.line(2 * cm, altura - 17.6 * cm, largura - 2 * cm, altura - 17.6 * cm)
    
    
    
    # Informações Importantes
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 18 * cm, "Informações Importantes")
    c.setFont("Arial", 10) 
    c.drawString(2 * cm, altura - 18.4 * cm, "Veículos não reclamados em até 60 dias após a remoção, poderá ser leiloado")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 18.8 * cm, "Prazo mínimo expira em: 01/01/9999")
    # Linha horizontal abaixo da Informações Importantes da Notificação de Autuação
    c.line(2 * cm, altura - 19 * cm, largura - 2 * cm, altura - 19 * cm)
    
    c.setFont("Helvetica-Bold", 10)   
    c.drawString(9 * cm, altura - 19.4 * cm, "EVITE NOVAS AUTUAÇÕES")
    # Linha horizontal abaixo de "EVITE NOVAS AUTUAÇÕES"
    c.line(2 * cm, altura - 19.6 * cm, largura - 2 * cm, altura - 19.6 * cm)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(5 * cm, altura - 20 * cm, "SOLICITE A RETIRADA DO VEÍCULO JUNTO À SECRETARIA DE SEGURANÇA")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(4 * cm, altura - 20.5 * cm, "Telefone: (12) 3892.6180 ou através do e-mail: transito@saosebasitao.sp.gov.br")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10 * cm, altura - 21 * cm, "Informações Adicionais acesse:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(6 * cm, altura - 21.5 * cm, "http://www.turismosaosebasitao.com.br/entrada-de-veiculos-de-turismo")
    
    # Inserir uma imagem (exemplo: logo da prefeitura)
    try:
        imagem = ImageReader("brasao.jpg")  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 1 * cm, altura - 6 * cm, width=2 * cm, height=3 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
    
 ########################### Rodapé#####################################
    # Imagem Brasão
    try:
        imagem = ImageReader("brasao.jpg")  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 1 * cm, altura - 25 * cm, width=2 * cm, height=3 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")

# Destinatário
    # retangulo destinatário
        #   (x  , y,   largura, altura, stroke=1, fill=0)
    c.rect(4*cm, 2*cm, 15*cm, 4*cm , stroke=1, fill=0)
    c.setFont("Arial", 8)
    c.drawString(4.2 * cm, 5.5 * cm, "DESTINATÁRIO")
    c.setFont("Arial", 10)
    c.drawString(4.2 * cm, 5 * cm, "PREFEITURA MUNICIPAL DE SÃO SEBASTIÃO")
    c.drawString( 4.2* cm, 4.5 * cm, "SECRETARIA DE SEGURANÇA URBANA")
    c.drawString(4.2 * cm, 4 * cm, "RUA AMAZONAS N°84 - INDUSTRIAL")
    c.drawString(4.2 * cm, 3.5 * cm, "CEP: 11609-509        SÃO SEBASTIÃO")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(6.5 * cm, 2.3 * cm, "NOTIFCAÇÃO DE REMOÇÃO DE VEÍCULO")
    # Linha horizontal acima de NOTIFCAÇÃO DE REMOÇÃO DE VEÍCULO"
    c.line(4 * cm, altura - 25 * cm, largura - 2.6 * cm, altura - 25 * cm)


    # Remetente
    c.setFont("Helvetica-Bold",8)
    c.drawString(9 * cm, 1.5 * cm, "REMETENTE")
    c.drawString(9 * cm, 1.1 * cm, "PREFEITURA MUNICIPAL DE SÃO SEBASTIÃO")
    c.drawString(9 * cm, 0.8 * cm, "SECRETARIA DE SEGURANÇA URBANA")
    c.drawString(9 * cm, 0.5 * cm, "RUA AMAZONAS N°84 - INDUSTRIAL")
    c.drawString(9 * cm, 0.2 * cm, "CEP: 11609-509        SÃO SEBASTIÃO")
    
    ######################### PRÓXIMA PÁGINA #################################
    c.showPage()
    # retangulo verso
        #   (x  , y,   largura, altura, stroke=1, fill=0)
    c.rect(4*cm, 2*cm, 20*cm, 20*cm , stroke=1, fill=0)
    
    
