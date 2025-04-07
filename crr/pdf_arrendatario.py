from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import LETTER,A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame



def render_notificacao_arrendatario(c, notificacao, width, height):
    largura, altura = LETTER 

    crr = notificacao.crr
    aits = notificacao.crr.ait.all()

    primeiro_ait = aits[0].ait if len(aits) > 0 else "Sem AIT"
    segundo_ait = aits[1].ait if len(aits) > 1 else "Sem AIT"
   
    enquadramento = crr.enquadramento.all()
  

    primeiro_enquadramento = enquadramento[0].enquadramento if len(enquadramento) > 0 else "Sem Enquadramento"
    segundo_enquadramento = enquadramento[1].enquadramento if len(enquadramento) > 1 else "Sem Enquadramento"

    # Configuração da página (agora usando LETTER)
    largura, altura = LETTER  # Dimensões: 8.5 x 11 polegadas
   
    
    # Registrar fonte personalizada
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c.setFont("Arial", 10)

     # Inserir uma imagem (exemplo: logo da prefeitura)
    try:
        imagem = ImageReader("media/brasao.jpg")  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 2 * cm, altura - 6 * cm, width=2 * cm, height=3 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
    
    # Título principal
    c.setFont("Helvetica-Bold", 14)
    c.drawString(6 * cm, altura - 3 * cm, "PREFEITURA MUNICIPAL DE SÃO SEBASTIÃO")

    c.setFont("Arial", 12)
    c.drawString(7 * cm, altura - 4 * cm, "SECRETARIA DE SEGURANÇA URBANA")

     # Linha horizontal acima de notificação de remoção de veículos ao pátio
    c.line(4 * cm, altura - 5.0 * cm, largura - 2 * cm, altura - 5.0 * cm)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(7 * cm, altura - 5.4 * cm, "NOTIFICAÇÃO DE REMOÇÃO DE VEÍCULOS AO PÁTIO")
    
    # Linha horizontal abaixo de notificação de autuação por infração de trânsito
    c.line(4 * cm, altura - 5.5 * cm, largura - 2 * cm, altura - 5.5 * cm)
    
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
    c.drawString(6 * cm, altura - 6.4 * cm, "N° C.R.R.") #\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 6.9 * cm, crr.numero_crr) #\\\\\\\\\\\\\\\\
    # Barra vertical em frente auto de infração
    c.line(9* cm, altura - 6.1 * cm, 9 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(9.5 * cm, altura - 6.4 * cm, "Data da Postagem:") #\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(9.5 * cm, altura - 6.9 * cm, f"{notificacao.data_postagem}") #\\\\\\\\\\\\\\\
    # Barra vertical em frente data de postagem 
    c.line(12.7* cm, altura - 6.1 * cm, 12.7 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(13 * cm, altura - 6.4 * cm, "Data Emissão:") #\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(13 * cm, altura - 6.9 * cm, f"{notificacao.data_emissao}")
    # Barra vertical em frente data emissão
    c.line(15.7* cm, altura - 6.1 * cm, 15.7 * cm, altura - 7 * cm)

    c.setFont("Arial", 8)
    c.drawString(16.5 * cm, altura - 6.4 * cm, "Numero Controle:")
    c.setFont("Arial", 10)
    c.drawString(16.5 * cm, altura - 6.9 * cm, str(notificacao.numero_controle))
    
    
    # Linha horizontal abaixo da identificação do veículo
    c.line(2 * cm, altura - 7.7 * cm, largura - 2 * cm, altura - 7.7 * cm)
    # Identificação do Veículo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 7.5 * cm, "Identificação do Veículo")
    
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 8 * cm, "Placa/Chassi:") #\\\\\\\\\\\\\\\\\\\\\\\
     # Barra vertical
    c.line(3.7* cm, altura - 7.7 * cm, 3.7 * cm, altura - 8.6 * cm)

    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 8.5 * cm, crr.placa_chassi) #\\\\\\\\\\\\\\\\\\\\\\\\\\

    c.setFont("Arial", 8)
    c.drawString(3.8 * cm, altura - 8 * cm, "Município / UF:") #\\\\\\\\\\\\\
    # Barra vertical
    c.line(7.8* cm, altura - 7.7 * cm, 7.8 * cm, altura - 8.6 * cm)

    c.setFont("Arial", 10)
    c.drawString(3.8 * cm, altura - 8.5 * cm, crr.municipio_veiculo) #\\\\\\\\\\\\\\\\\\\
    
    c.setFont("Arial", 8)
    c.drawString(7.9 * cm, altura - 8 * cm, "Marca/Modelo:") #\\\\\\\\\\\\\\\
    
    
    c.setFont("Arial", 10)
    c.drawString(7.9 * cm, altura - 8.5 * cm, f"{crr.marca}/{crr.modelo}") #\\\\\\\\\\\\\\\

    # Barra vertical
    c.line(10.5* cm, altura - 7.7 * cm, 10.5 * cm, altura - 8.6 * cm)

   
    # Barra vertical
    c.line(14.2* cm, altura - 7.7 * cm, 14.2 * cm, altura - 8.6 * cm)
    

    c.setFont("Arial", 8)
    c.drawString(14.3 * cm, altura - 8 * cm, "Espécie:") #\\\\\\\\\\\\\\\\\\\\\\\\\
    # Barra vertical
    c.line(16.9* cm, altura - 7.7 * cm, 16.9 * cm, altura - 8.6 * cm)

    c.setFont("Arial", 10)
    c.drawString(14.3 * cm, altura - 8.5 * cm, crr.especie) #\\\\\\\\\\\\\\\\\\\\\

    c.setFont("Arial", 8)
    c.drawString(17 * cm, altura - 8 * cm, "Categoria:") #\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(17 * cm, altura - 8.5 * cm, crr.categoria) #\\\\\\\\\\\\\\\
    
    # Linha horizontal acima de identificação do local da infração
    c.line(2 * cm, altura - 8.6 * cm, largura - 2 * cm, altura - 8.6 * cm)
     # Local da Infração
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 9 * cm, "Identificação do Local da remoção")
        # Linha horizontal abaixo de identificação do local da infração
    c.line(2 * cm, altura - 9.1 * cm, largura - 2 * cm, altura - 9.1 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 9.4 * cm, "Local da remoção") #\\\\\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 9.9 * cm, '') # \\\\\\\\\\\\\\\\\\\\\\\\
        # Linha horizontal acima de local da infração
    c.line(2 * cm, altura - 10 * cm, largura - 2 * cm, altura - 10 * cm)

 # Linha horizontal acima de "Município / UF / Código:"
    c.line(2 * cm, altura - 11 * cm, largura - 9.6 * cm, altura - 11 * cm)
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 11.3* cm, "Município / UF / Código:")
    # Barra vertical
    c.line(6.9* cm, altura - 11 * cm, 6.9 * cm, altura - 11.8 * cm)

    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 11.8 * cm, "SÃO SEBASTIÃO / SP / 7115")

    c.setFont("Arial", 8)
    c.drawString(7.1 * cm, altura - 11.3 * cm, "Data da remoção:") #\\\\\\\\\\\\\\
    # Barra vertical
    c.line(9.5 * cm, altura - 11 * cm, 9.5 * cm, altura - 11.9 * cm)

    c.setFont("Arial", 10)
    c.drawString(7.1 * cm, altura - 11.8 * cm, f"{crr.data_remocao}") #\\\\\\\\\\\\\\\\\\\\

    c.setFont("Arial", 8)
    c.drawString(9.7 * cm, altura - 11.3 * cm, "Hora da remoção:") #\\\\\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(9.7 * cm, altura - 11.8 * cm, f"{crr.hora_remocao}")  #\\\\\\\\\\\\\\\\\\\\\\\

    # retangulo para imagem
        #   (x  , y,   largura, altura, stroke=1, fill=0)
    c.rect(12*cm, 12.53*cm, 7.5*cm, 4.41*cm , stroke=1, fill=0)

    # Imagem Brasão
    imagem = notificacao.imagem
    try:
        imagem = ImageReader(imagem)  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 12.1 * cm, altura - 15.4 * cm, width=7.3 * cm, height=4.4 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 10.3 * cm, "Observação:") #\\\\\\\\\\\\\\\\\\\\\\\\
    c.drawString(2 * cm, altura - 10.8 * cm, str(crr.observacao))
    
    # Definir estilos de texto
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    
    # Linha horizontal acima da tipificação da infração
    c.line(2 * cm, altura - 11.9 * cm, largura - 9.6 * cm, altura - 11.9 * cm)

    # Tipificação da Infração
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.5 * cm, altura - 12.35 * cm, "Tipificação da Infração")
    # Linha horizontal abaixo da tipificação da infração
    c.line(2 * cm, altura - 12.5 * cm, largura - 9.6 * cm, altura - 12.5 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 12.8 * cm, "Descrição da Infração:")
    # Barra vertical
    c.line(6.8* cm, altura - 12.5 * cm, 6.8 * cm, altura - 14.7 * cm)

    # ------ DESCRIÇÃO DA INFRAÇÃO ------ #\\\\\\\\\\\\\\\\\\\\\\\\\\
    texto_descricao = notificacao.descricao_infracao

    paragrafo = Paragraph(texto_descricao, style_normal)

    # Definir uma área onde o texto será exibido (posição X, Y, largura, altura)
    frame = Frame(1.8*cm, 11.3*cm, 5*cm, 4*cm)

    # Adicionar o parágrafo ao frame
    frame.addFromList([paragrafo], c)
    # ------------------------------------------------------
    
    
    c.setFont("Arial", 8)
    c.drawString(7 * cm, altura - 12.8 * cm, "Enquadramento:")
    # Barra vertical
    c.line(9.3* cm, altura - 12.5 * cm, 9.3 * cm, altura - 14.7 * cm)

    c.setFont("Arial", 10)
    c.drawString(7 * cm, altura - 13.3 * cm,f"{primeiro_enquadramento}")
    c.drawString(7 * cm, altura - 13.8 * cm, f"{segundo_enquadramento}")

    c.setFont("Arial", 8)
    c.drawString(9.5* cm, altura - 12.8 * cm, "Auto de infração:") #\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(9.5* cm, altura - 13.3 * cm, f"{primeiro_ait}") # \\\\\\\\\\\\\\\\\\\\\
    c.drawString(9.5* cm, altura - 13.8 * cm, f"{segundo_ait}") # \\\\\\\\\\\\\\\\\\\\\
    


     # Linha horizontal acima de Amparo Legal
    c.line(2 * cm, altura - 14.7 * cm, largura - 9.6 * cm, altura - 14.7 * cm)
    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 15 * cm, "Amparo Legal:") # \\\\\\\\\\\\\\\\\\
    # Barra vertical
    c.line(5* cm, altura - 14.7 * cm, 5 * cm, altura - 15.5* cm)

    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 15.4* cm, notificacao.amparo_legal) #Art. 279-A C.T.B. \\\\\\\\

    c.setFont("Arial", 8)
    c.drawString(6 * cm, altura - 15 * cm, "Identificação da Autoridade/Agente Autuador:") # \\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 15.4 * cm, crr.agente_autuador) # \\\\\\\\\\\\\\\\\\
    
    
    # Linha horizontal acima da identificação de condutor 
    c.line(2 * cm, altura - 15.5 * cm, largura - 2 * cm, altura - 15.5 * cm)
    # Identificação do Condutor
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 15.9 * cm, "Identificação do Condutor")
    # Linha horizontal abaixo de indentificação de condutor
    c.line(2 * cm, altura - 16 * cm, largura - 2 * cm, altura - 16 * cm)

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 16.3 * cm, "Nº Habilitação do Condutor:") 
    # Barra vertical
    c.line(5.7* cm, altura - 16 * cm, 5.7 * cm, altura - 16.8 * cm)

    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 16.7 * cm, crr.habilitacao_condutor) 
     #Linha horizontal abaixo da habilitação do condutor
    c.line(2 * cm, altura - 16.8 * cm, largura - 2 * cm, altura - 16.8 * cm)

    c.setFont("Arial", 8)
    c.drawString(6 * cm, altura - 16.3 * cm, "UF:") #\\\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(6 * cm, altura - 16.7 * cm, crr. uf_cnh) #\\\\\\\\\\\\\

    c.setFont("Arial", 8)
    c.drawString(7 * cm, altura - 16.3 * cm, "CPF:") # \\\\\\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(7 * cm, altura - 16.7 * cm, crr.cpf) #\\\\\\\\\\\\\\\\\\\\\\\\\
    

    c.setFont("Arial", 8)
    c.drawString(2 * cm, altura - 17.1 * cm, "Nome:") # \\\\\\\\\\\\\\\\\
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 17.5 * cm, crr.nome_condutor) # \\\\\\\\\\\\\\\\\\\\\\\
    #Linha horizontal abaixo de NOME
    c.line(2 * cm, altura - 17.6 * cm, largura - 2 * cm, altura - 17.6 * cm)
    
    
    
    # Informações Importantes
    c.setFont("Helvetica-Bold", 10)
    c.drawString(8 * cm, altura - 18 * cm, "Informações Importantes")
    c.setFont("Arial", 10) 
    c.drawString(2 * cm, altura - 18.4 * cm, "Veículo não reclamado (solicitado) em até 60 dias após a remoção poderá ser leiloado. (Art. 328 C.T.B.)")
    c.setFont("Arial", 10)
    c.drawString(2 * cm, altura - 18.9 * cm, "Apto para leilão a partir de: 23/04/2025") #\\\\\\\\\\\\
    c.drawString(2 * cm, altura - 19.4 * cm, "Nome do pátio: Patio E Guincho Universal LTDA")
    c.drawString(2 * cm, altura - 19.9 * cm, "Local do pátio: Rua Bolivia, Jaraguá - São Sebastião/SP - CEP: 11600-748")
    
    # Linha horizontal abaixo da Informações Importantes da Notificação de Autuação
    c.line(2 * cm, altura - 20.4 * cm, largura - 2 * cm, altura - 20.4* cm)
    
    c.setFont("Helvetica-Bold", 10)   
    c.drawString(8 * cm, altura - 20.8 * cm, "OUTRAS INFORMAÇÕES")
    # Linha horizontal abaixo de "OUTRAS INFORMAÇÕES"
    c.line(2 * cm, altura - 20.9 * cm, largura - 2 * cm, altura - 20.9 * cm)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(3 * cm, altura - 22 * cm, "SOLICITE A RETIRADA DO VEÍCULO JUNTO À DIVISÃO DE PROCESSAMENTO DE MULTAS")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(3 * cm, altura - 22.5 * cm, "Telefone: (12) 3892-6180 / 3892-1540 ou através do e-mail: transito@saosebasitao.sp.gov.br")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(3 * cm, altura - 23.5 * cm, "PROTOCOLO DE LIBERAÇÃO DE VEÍCULOS REMOVIDOS ATRAVÉS DO 1DOC:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(3 * cm, altura - 24 * cm, "https://saosebastiao.1doc.com.br/b.php?pg=o/wp")
    
   
    
     ######################### PRÓXIMA PÁGINA #################################
    c.showPage()
 ########################### Rodapé#####################################
   

# Destinatário
    # retangulo destinatário
        #   (x  , y,   largura, altura, stroke=1, fill=0)
    c.rect(2*cm, 25*cm, 17*cm, 3.5*cm , stroke=1, fill=0)
    c.setFont("Arial", 8)
    c.drawString(2.2 * cm, 28.2 * cm, "DESTINATÁRIO")
    c.setFont("Arial", 10)
    c.drawString(2.2 * cm, 27.7 * cm, notificacao.destinatario)
    
    c.drawString(2.2 * cm, 26.6 * cm, f"{notificacao.endereco}, {notificacao.numero}    {notificacao.complemento}  -   {notificacao.bairro}")
    c.drawString(2.2 * cm, 26.1 * cm,f"{notificacao.cep}           {notificacao.cidade_destinatario} / {notificacao.uf_destinatario}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(6 * cm, 25.15 * cm, "NOTIFCAÇÃO DE REMOÇÃO DE VEÍCULO")
    # Linha horizontal acima de NOTIFCAÇÃO DE REMOÇÃO DE VEÍCULO"
    c.line(2 * cm, altura - 2.3 * cm, largura - 2.6 * cm, altura - 2.3 * cm)

    # Remetente
    c.setFont("Helvetica-Bold",8)
    c.drawString(8.5 * cm, 23.9 * cm, "REMETENTE")
    c.drawString(8.5 * cm, 23.6 * cm, "PREFEITURA MUNICIPAL DE SÃO SEBASTIÃO")
    c.drawString(8.5 * cm, 23.3 * cm, "SECRETARIA DE SEGURANÇA URBANA")
    c.drawString(8.5 * cm, 23 * cm, "RUA AMAZONAS N°84 - INDUSTRIAL")
    c.drawString(8.5 * cm, 22.7 * cm, "CEP: 11609-509        SÃO SEBASTIÃO / SP")

    c.setDash(3, 3)  # Define o padrão de tracejado (3 pontos desenhados, 3 pontos vazios)
    c.line(2 * cm, altura - 5.8 * cm, largura - 2 * cm, altura - 5.8 * cm)  # Desenha a linha 

 # Remetente
    c.setFont("Helvetica-Bold",12)
    c.drawString(7 * cm, 20.3 * cm, "Desacelere. Seu bem maior é a vida.")

# Imagem do trânsito 2ª pagina (VERSO) 
    try:
        imagem = ImageReader("media/verso.jpeg")  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 1 * cm, altura - 16.2* cm, width=19* cm, height=10 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}") 
#____________________________________________________________________________________#

    c.setDash(3, 3)  # Define o padrão de tracejado (3 pontos desenhados, 3 pontos vazios)
    c.line(2 * cm, altura - 16.9 * cm, largura - 2 * cm, altura - 16.9 * cm)  # Desenha a linha
    c.setDash()
# Rodapé da 2ª pagina 
 # Imagem do rodapé 2ª pagina 
    try:
        imagem = ImageReader("media/cabeçalho.jpg")  # Substitua pelo caminho da sua imagem
        c.drawImage(imagem, 2 * cm, altura - 25.5 * cm, width=17 * cm, height=13.5 * cm, preserveAspectRatio=True)
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")

    # retangulo destinatário
        #   (x  , y,   largura, altura, stroke=1, fill=1)
    c.rect(3*cm, 3*cm, 15*cm, 3*cm , stroke=1, fill=0)
    # Destinatário 2ª pagina
    c.setFont("Arial", 8)
    c.drawString(3.2 * cm, 5.6 * cm, "DESTINATÁRIO")
    c.setFont("Arial", 10)
    c.drawString(3.2 * cm, 5 * cm, notificacao.destinatario)
    
    c.drawString(3.2 * cm, 4 * cm,f"{notificacao.endereco}, {notificacao.numero} - {notificacao.complemento} - {notificacao.bairro}")
    c.drawString(3.2 * cm, 3.5 * cm, f"{notificacao.cep}              {notificacao.cidade_destinatario} / {notificacao.uf_destinatario}")
    
   
    
    
