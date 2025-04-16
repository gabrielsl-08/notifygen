from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from .models import Notificacao, Crr, Ait, Enquadramento,Arrendatario,TabelaEnquadramento
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
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from datetime import timedelta

# ============== FUNÇÕES DE AÇÃO ============== #
def gerar_pdf_notificacoes(modeladmin, request, queryset):   
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
gerar_pdf_notificacoes.short_description = "NOTIFICAÇÃO PROPRIETÁRIO"


# ============== INLINES ============== #

class AitAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/mascaras.js',)  # Caminho relativo à pasta "static"

class AitInline(admin.TabularInline):
    model = Ait
    extra = 1
    fields = ['ait']
    class Media:
        js = ('js/mascaras.js',)



class EnquadramentoInline(admin.TabularInline):
    model = Enquadramento
    extra = 1
    max_num = 4
    fields = ['enquadramento']
    verbose_name_plural = "Enquadramentos"
 

class ArrendatárioAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/mascaras.js',)  # Caminho relativo à pasta "static"
        
class ArrendatarioInline(admin.TabularInline):
    model = Arrendatario
    extra = 1
    max_num = 1
    fields = ['nome_arrendatario','cnpj_arrendatario','endereco_arrendatario','numero_arrendatario',
              'complemento_arrendatario','bairro_arrendatario','cidade_arrendatario','uf_arrendatario','cep_arrendatario' ]
    verbose_name_plural = "Arrendatário"
    class Media:
        js = (
            'js/jquery.mask.min.js',
            'js/custom-mask.js',
            'js/mascaras.js',
        )

# ============== MODELADMINS ============== #
class FiltroCrrAtrasado(admin.SimpleListFilter):
    title = 'FILTRAR CRR'
    parameter_name = 'crr_filtro'

    def lookups(self, request, model_admin):
        return (
            ('atrasado', 'CRR PARA EMITIR NOTIFICAÇÃO'),
            ('edital', 'CRR PARA EMITIR EDITAL'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'atrasado':
            data_limite = date.today() - timedelta(days=10)
            return queryset.filter(data_remocao__lte=data_limite, not_gerada=False, status='retido')

        if self.value() == 'edital':
            data_limite = date.today() - timedelta(days=30)
            return queryset.filter(data_remocao__lte=data_limite, status='retido', edital_emitido=False)

        return queryset  # Retorna todos os CRRs quando nenhum filtro é selecionado


class TabelaEnquadramentoResource(resources.ModelResource):
    class Meta:
        model = TabelaEnquadramento
        import_id_fields = ['codigo']  # chave única para atualizar se quiser
        fields = ('codigo', 'amparo_legal', 'descricao_infracao')  # campos para importar/exportar


@admin.register(TabelaEnquadramento)
class TabelaEnquadramentoAdmin(ImportExportModelAdmin):
    resource_class = TabelaEnquadramentoResource
    list_display = ('codigo', 'amparo_legal', 'descricao_infracao')

@admin.register(Crr)
class CrrAdmin(admin.ModelAdmin):
    list_display = ('numero_crr','data_remocao', 'placa_chassi', 'marca', 'modelo', 'especie', 'get_enquadramentos','status','edital_emitido')
    
    list_filter = (FiltroCrrAtrasado,'data_remocao', 'status',)
    actions = ['gerar_edital_docx_action']
    list_editable = ('status',)
    
    ordering = ('numero_crr',)
    inlines = [AitInline,EnquadramentoInline,ArrendatarioInline]  # Corrigido: ambas inlines juntas

    def get_enquadramentos(self, obj):
        enquads = obj.enquadramentos.all()
        return ", ".join([str(enq.enquadramento.codigo) for enq in enquads]) if enquads else "—"
    get_enquadramentos.short_description = "Enquadramento"

    fieldsets = (
        ("CRR", {
            'fields': ('numero_crr','agente_autuador','status')
        }),
        ("Dados do Veículo", {
            'fields': ('placa_chassi', 'marca', 'modelo', 'especie', 'categoria', 'uf_veiculo', 'municipio_veiculo')
        }),
        ("Local da Infração", {
            'fields': ('local_remocao', 'data_remocao','hora_remocao','observacao')
        }),
        ("Condutor", {
            'fields': ('nome_condutor','habilitacao_condutor', 'uf_cnh', 'cpf')
        }),
        
    )
    
    class Media:
        js = (
            'js/jquery.mask.min.js',
            'js/custom-mask.js',
            'js/mascaras.js',
        )


    @admin.action(description="Gerar Edital em DOCX")
    def gerar_edital_docx_action(self, request, queryset):
        response = gerar_edital_docx(queryset)  # Gera o documento primeiro
        queryset.update(edital_emitido=True)  # Só agora marca como emitido
        return response
         


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('crr__numero_crr','numero_controle',  'data_emissao','get_ait','imagem_preview','prazo_leilao')
    list_display_links = ('crr__numero_crr',)
    search_fields = ('crr__numero_crr','numero_controle', 'destinatario')
    list_filter = ('data_emissao', 'crr__numero_crr')
    readonly_fields = ('numero_controle','imagem_preview')
    actions = [gerar_pdf_notificacoes]

   
    
    def get_ait(self, obj):
        # Retorna todos os AITs associados ao CRR da Notificação 
        aits = obj.crr.ait.all()  # Busca todos os AITs relacionados ao CRR
        return ", ".join([ait.ait for ait in aits]) if aits else ""
    get_ait.short_description = "AIT"  # Nome da coluna no Django Admin 

    def get_enquadramento(self, obj):
       #  Retorna todos os enquadramentos associados ao CRR da Notificação 
        enquadramentos = obj.crr.enquadramento.all()  # Busca todos os enquadramentos
        return ", ".join([enq.codigo for enq in enquadramentos]) if enquadramentos else ""    
    get_enquadramento.short_description = "ENQUADRAMENTO"  # Nome da coluna no admin
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Se for uma nova notificação (não editando uma existente)
        if obj is None:
            form.base_fields['prazo_leilao'].required = False
        
        return form

    def save_model(self, request, obj, form, change):
        if obj.crr.status != 'retido':
            raise forms.ValidationError("Somente para veículos com status 'Retido'.")
        
        if obj.crr and obj.crr.data_remocao:
            obj.prazo_leilao = obj.crr.data_remocao + timedelta(days=60)
        else:
            raise forms.ValidationError("O CRR relacionado não possui data de remoção definida.")
        
        super().save_model(request, obj, form, change)

    fieldsets = (
        ("Informações da Notificação", {
            'fields': ('numero_controle', 'crr', 'data_emissao', 'data_postagem','prazo_leilao', 'imagem')
        }),
        ("Destinatário", {
            'fields': ('destinatario', 'endereco', 'numero', 'complemento', 'bairro', 'cidade_destinatario', 'cep')
        }),
       
    )

    
    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 100px; max-width: 100px;" /></a>',
                obj.imagem.url,
                obj.imagem.url
            )
        return "Sem imagem"

    imagem_preview.short_description = "Pré-visualização"

   









 