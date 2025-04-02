from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from .models import Notificacao, Crr, Ait, Enquadramento
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone
from .widgets import AmparoLegalWidget
from django import forms

# ============== FUNÇÕES DE AÇÃO ============== #
def export_to_csv(modeladmin, request, queryset):
    """Exporta notificações selecionadas para CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="notificacoes_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'CRR', 'Controle', 'Data Emissão', 
        'Placa', 'Marca/Modelo', 'Espécie',
        'Condutor', 'CPF', 'CNH'
    ])
    
    for notificacao in queryset:
        veiculo = notificacao.crr
        
        writer.writerow([
            veiculo.numero_crr,
            notificacao.numero_controle,
            notificacao.data_emissao.strftime('%d/%m/%Y') if notificacao.data_emissao else '',
            veiculo.placa_chassi,
            f"{veiculo.marca}/{veiculo.modelo}",
            veiculo.get_especie_display(),
            veiculo.nome_condutor,
            veiculo.cpf,
            veiculo.habilitacao_condutor,
        ])
    
    return response
export_to_csv.short_description = "Exportar para CSV"

def gerar_pdf_notificacoes(modeladmin, request, queryset):
    """Gera PDF para as notificações selecionadas"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    
    for i, notificacao in enumerate(queryset):
        if i > 0:
            c.showPage()
        
        render_notificacao_template(c, notificacao, largura, altura) 
    
    c.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="notificacoes_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    return response
gerar_pdf_notificacoes.short_description = "Gerar PDF das notificações"

# ============== INLINES ============== #
class AitInline(admin.TabularInline):
    model = Ait
    extra = 1
    max_num = 4
    fields = ['ait']
    verbose_name_plural = "Autos de Infração"

class EnquadramentoInline(admin.TabularInline):
    model = Enquadramento
    extra = 1
    max_num = 4
    fields = ['enquadramento']
    verbose_name_plural = "Enquadramentos Jurídicos"

# ============== MODELADMINS ============== #
@admin.register(Crr)
class CrrAdmin(admin.ModelAdmin):
    list_display = ('numero_crr', 'placa_chassi', 'marca', 'modelo', 'especie', 'status')
    search_fields = ('numero_crr', 'placa_chassi', 'marca', 'modelo')
    list_filter = ('especie', 'uf_veiculo', 'status')
    list_editable = ('status',)
    ordering = ('numero_crr',)
    inlines = [AitInline, EnquadramentoInline]  # Corrigido: ambas inlines juntas
    
    fieldsets = (
        ("Dados do CRR", {
            'fields': ('numero_crr', 'data_remocao', 'hora_remocao', 'agente_autuador', 'observacao','status')
        }),
        ("Dados do Veículo", {
            'fields': ('placa_chassi', 'marca', 'modelo', 'especie', 'categoria','uf_veiculo','municipio_veiculo',)
        }),
        ("Localização/Status", {
            'fields': (  'local_remocao',)
        }),
    )



@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
  
    list_display = ('numero_controle',  'data_emissao',  'imagem_preview')
    search_fields = ('numero_controle', 'crr__numero_crr', 'destinatario')
    list_filter = ('data_emissao', 'uf_destinatario')
    readonly_fields = ('imagem_preview',)
    actions = [export_to_csv, gerar_pdf_notificacoes]
    
    fieldsets = (
        (None, {
            'fields': ('numero_controle', 'crr', 'data_emissao', 'data_postagem','descricao_infracao')
        }),
        ("Destinatário", {
            'fields': ('destinatario', 'endereco', 'complemento', 'cep')
        }),
        ("Detalhes", {
            'fields': ('amparo_legal', 'prazo_leilao','imagem', 'imagem_preview')
        }),
    )

    
    
    def imagem_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-height:100px; max-width:100px;" />', 
            obj.imagem.url
        ) if obj.imagem else "Sem imagem"
    imagem_preview.short_description = "Pré-visualização"











 



