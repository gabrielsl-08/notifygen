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
from .pdf_templates import render_notificacao_template
from django.urls import reverse
from django.template.response import TemplateResponse
from datetime import date, timedelta
from .utils import gerar_edital_docx

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
class FiltroCrrAtrasado(admin.SimpleListFilter):
    title = 'Filtrar CRRs'
    parameter_name = 'crr_filtro'

    def lookups(self, request, model_admin):
        return (
            ('atrasado', 'CRR Atrasado (>10 dias e sem Notificação)'),
            ('edital', 'CRR Edital (>30 dias e Retido)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'atrasado':
            data_limite = date.today() - timedelta(days=10)
            return queryset.filter(data_remocao__lte=data_limite, not_gerada=True, status='retido')

        if self.value() == 'edital':
            data_limite = date.today() - timedelta(days=30)
            return queryset.filter(data_remocao__lte=data_limite, status='retido', edital_emitido=False)

        return queryset  # Retorna todos os CRRs quando nenhum filtro é selecionado

@admin.register(Crr)
class CrrAdmin(admin.ModelAdmin):
    list_display = ('numero_crr','data_remocao', 'placa_chassi', 'marca', 'modelo', 'especie', 'status','edital_emitido')
    search_fields = ('numero_crr', 'placa_chassi', 'marca', 'modelo','status')
    list_filter = (FiltroCrrAtrasado,'data_remocao', 'status',)
    actions = ['gerar_edital_docx_action']
    list_editable = ('status',)
    ordering = ('numero_crr',)
    inlines = [AitInline, EnquadramentoInline]  # Corrigido: ambas inlines juntas
    
    @admin.action(description="Gerar Edital em DOCX")
    def gerar_edital_docx_action(self, request, queryset):
        queryset.update(edital_emitido=True)
        return gerar_edital_docx(queryset)
         

    fieldsets = (
        ("Dados do CRR", {
            'fields': ('numero_crr', 'data_remocao', 'hora_remocao', 'agente_autuador', 'observacao','status')
        }),
        ("Dados do Veículo", {
            'fields': ('placa_chassi', 'marca', 'modelo', 'especie', 'categoria','uf_veiculo','municipio_veiculo',)
        }),
         ("Local Da Remoção", {
            'fields': ('local_remocao',)
        }),
        ("CONDUTOR", {
            'fields': ('habilitacao_condutor','uf_cnh','cpf','nome_condutor',)
        
        }),
        
        
    )




@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('crr__numero_crr','numero_controle',  'data_emissao','get_ait','imagem_preview')
    search_fields = ('crr__numero_crr','numero_controle', 'destinatario')
    list_filter = ('data_emissao', 'crr__numero_crr')
    readonly_fields = ('numero_controle',)
   
    actions = [export_to_csv,gerar_pdf_notificacoes]

    def get_ait(self, obj):
        """ Retorna todos os AITs associados ao CRR da Notificação """
        aits = obj.crr.ait.all()  # Busca todos os AITs relacionados ao CRR
        return ", ".join([ait.ait for ait in aits]) if aits else "Sem AIT"

    get_ait.short_description = "AITs"  # Nome da coluna no Django Admin 

    def get_enquadramento(self, obj):
        """ Retorna todos os enquadramentos associados ao CRR da Notificação """
        enquadramentos = obj.crr.enquadramento.all()  # Busca todos os enquadramentos
        return ", ".join([enq.codigo for enq in enquadramentos]) if enquadramentos else "Sem enquadramento"
    
    get_enquadramento.short_description = "Enquadramentos"  # Nome da coluna no admin
    
    def save_model(self, request, obj, form, change):
        """Impede a criação de Notificação se o veículo não estiver 'Retido'."""
        if obj.crr.status != 'retido':
            raise ValidationError("A Notificação só pode ser emitida para veículos com status 'Retido'.")
        
        super().save_model(request, obj, form, change)

    fieldsets = (
        ("Informações da Notificação", {
            'fields': ('numero_controle', 'crr', 'data_emissao', 'data_postagem', 'descricao_infracao', 'imagem')
        }),
        ("Destinatário", {
            'fields': ('destinatario', 'endereco', 'numero', 'complemento', 'bairro', 'cidade_destinatario', 'cep')
        }),
        ("Detalhes", {
            'fields': ('amparo_legal', 'prazo_leilao')
        }),
    )

    

    def imagem_preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px; max-width:100px;" />', obj.imagem.url) if obj.imagem else "Sem imagem"
    imagem_preview.short_description = "Pré-visualização"   











 



