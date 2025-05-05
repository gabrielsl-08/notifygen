from django.contrib import admin
from django.http import HttpResponse
from .models import Notificacao
from crr.models import Crr, ImagemCrr, Condutor
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone
from .pdf_templates import render_notificacao_template
from django.core.exceptions import ValidationError
from datetime import date, timedelta


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

# Register your models here.
@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('crr__numero_crr','numero_controle','data_emissao','data_postagem','imagem_preview','prazo_leilao')
    list_display_links = ('crr__numero_crr',)
    search_fields = ('crr__numero_crr','numero_controle', 'destinatario')
    list_filter = ('data_emissao', 'crr__numero_crr')
    readonly_fields = ('numero_controle','prazo_leilao')
    actions = [gerar_pdf_notificacoes]

    def get_ait(self, obj):
        aits = obj.crr.ait.all()
        return ", ".join([ait.ait for ait in aits]) if aits else ""
    get_ait.short_description = "AIT"

    def get_enquadramento(self, obj):
        enquadramentos = obj.crr.enquadramento.all()
        return ", ".join([enq.codigo for enq in enquadramentos]) if enquadramentos else ""
    get_enquadramento.short_description = "ENQUADRAMENTO"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None and 'prazo_leilao' in form.base_fields:
            form.base_fields['prazo_leilao'].required = False
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.prazo_leilao = obj.crr.data_remocao + timedelta(days=60)

        if obj.crr.status != 'retido':
            raise ValidationError("Somente veículos com status 'Retido'.")

        # ✅ Atualiza o status not_gerada do CRR relacionado
        obj.crr.not_gerada = True
        obj.crr.save()

        super().save_model(request, obj, form, change)


    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        crr_id = request.GET.get("crr")
        if crr_id:
            initial["crr"] = crr_id
        return initial

    def response_add(self, request, obj, post_url_continue=None):
        # Gera o PDF em memória
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        largura, altura = A4
        render_notificacao_template(c, obj, largura, altura)
        c.save()
        buffer.seek(0)

        # Retorna como arquivo para download no navegador
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="notificacao_{obj.numero_controle}.pdf"'
        return response

    fieldsets = (
        ("Informações da Notificação", {
            'fields': ('numero_controle','crr','data_emissao','data_postagem')
        }),
        ("Destinatário", {
            'fields': ('destinatario', 'endereco', 'numero', 'complemento', 'bairro', 'cidade_destinatario','uf_destinatario', 'cep')
        }),
    )


    def imagem_preview(self, obj):
        imagem = obj.crr.imagens.first()
        if imagem and imagem.imagem:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 60px; max-width: 60px;" /></a>',
                imagem.imagem.url
            )
        return "Sem imagem"

    imagem_preview.short_description = "Pré-visualização"

    class Media:
        js = (
            
            'js/mascaras.js',
        
        )