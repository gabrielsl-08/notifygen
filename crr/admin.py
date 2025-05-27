from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from .models import  (Crr,Ait,Condutor, Enquadramento,Arrendatario,Veiculo,
                      TabelaEnquadramento,TabelaArrendatario, ImagemCrr
                    )

from django import forms
from django.urls import reverse
from datetime import date, timedelta
from crr.utils import gerar_edital_docx
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.postgres.forms import SplitArrayWidget


# ============== INLINES ============== #
'''
@admin.register(AgenteAutuador)
class AgenteAutuadorAdmin(admin.ModelAdmin):
    list_display = ('nomeAgente', 'matriculaAgente', 'orgao')
    search_fields = ('nomeAgente', 'matriculaAgente', 'orgao')


class AgenteAutuadorInline(admin.TabularInline):
    model = AgenteAutuador
    extra = 0
    max_num = 1  # Quantas linhas vazias para novos condutores
    fields = ['matriculaAgente']
'''

class CondutorInline(admin.TabularInline):
    model = Condutor
    extra = 0
    max_num = 1  # Quantas linhas vazias para novos condutores
    fields = ['nomeCondutor','cnh','cnhEstrangeira', 'ufCnh', 'cpfCondutor']

class VeiculoInline(admin.TabularInline):
    model = Veiculo
    extra = 0
    max_num = 1  # Quantas linhas vazias para novos condutores
    fields = ['placa','chassi','marca', 'modelo', 'cor','especie','categoria','ufVeiculo','municipioVeiculo']

class AitAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/mascaras.js',)
class AitInline(admin.TabularInline):
    model = Ait
    extra = 1
    max_num = 4 
    fields = ['ait']
    class Media:
        js = ('js/mascaras.js',)

class EnquadramentoInlineForm(forms.ModelForm): # ajusta o tamanho do campo Enquadramento

    
    class Meta:
        model = Enquadramento
        fields = ['enquadramento']
        widgets = {
            'enquadramento': forms.Select(attrs={'style': 'width: 500px;'}),
        }        

class EnquadramentoInline(admin.TabularInline):

    
    model = Enquadramento
    form = EnquadramentoInlineForm
    extra = 1
    max_num = 4
    fields = ['enquadramento']
    verbose_name_plural = "Enquadramentos"

class ArrendatárioAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/mascaras.js',)

class ArrendatarioInline(admin.TabularInline):
    model = Arrendatario
    extra = 1
    max_num = 1
    fields = ['arrendatario']
    verbose_name_plural = "Arrendatário"
    class Media:
        js = (
            'js/mascaras.js',
        )


class TabelaArrendatarioResource(resources.ModelResource):
    class Meta:
        model = TabelaArrendatario
        import_id_fields = ['nome_arrendatario']
        fields = ('nome_arrendatario', 'cnpj_arrendatario','endereco_arrendatario','numero_arrendatario','complemento_arrendatario','bairro_arrendatario','cidade_arrendatario','uf_arrendatario','cep_arrendatario')

@admin.register(TabelaArrendatario)
class TabelaArrendatarioAdmin(ImportExportModelAdmin):
    resource_class = TabelaArrendatarioResource
    list_display = ('nome_arrendatario', 'cnpj_arrendatario')





# ============== MODELADMINS ============== #
class FiltroCrrAtrasado(admin.SimpleListFilter):
    title = 'TODOS CRRs'
    parameter_name = 'crr_filtro'

    def lookups(self, request, model_admin):
        return (
            ('atrasado', 'NOTIFICAÇÃO PENDENTE'),
            ('edital', 'EDITAL PENDENTE'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'atrasado':
            data_limite = date.today() - timedelta(days=10)
            return queryset.filter(data_remocao__lte=data_limite, not_gerada=False, status='retido')

        if self.value() == 'edital':
            data_limite = date.today() - timedelta(days=30)
            return queryset.filter(dataFiscalizacao__lte=data_limite, status='retido', edital_emitido=False)

        return queryset

class TabelaEnquadramentoResource(resources.ModelResource):
    class Meta:
        model = TabelaEnquadramento
        import_id_fields = ['codigo']
        fields = ('codigo', 'amparo_legal', 'descricao_infracao')

@admin.register(TabelaEnquadramento)
class TabelaEnquadramentoAdmin(ImportExportModelAdmin):
    resource_class = TabelaEnquadramentoResource
    list_display = ('codigo', 'amparo_legal', 'descricao_infracao')

class ImagemCrrInline(admin.StackedInline):
    model = ImagemCrr
    extra = 1
    max_num = 4
    fields = ['imagem', 'nomeArquivo', 'url']


    
@admin.register(Crr)
class CrrAdmin(admin.ModelAdmin):
  
    list_display = ('numeroCrr','criar_notificacao_link','dataFiscalizacao', 'get_enquadramentos','status','edital_emitido')
    list_filter = (FiltroCrrAtrasado,'dataFiscalizacao', 'status',)
    actions = ['gerar_edital_docx_action']
    list_editable = ('status',)
    ordering = ('numeroCrr',)
    inlines = [CondutorInline, VeiculoInline,AitInline,EnquadramentoInline,ArrendatarioInline,ImagemCrrInline]
   
    
    fieldsets = (
        ("CRR", {
            'fields': ('numeroCrr','matriculaAgente')
        }),        
        ("Local da Infração", {
            'fields': ('localFiscalizacao', 'dataFiscalizacao','horaFiscalizacao','observacao')
        }),
        )

    '''''
    def get_readonly_fields(self, request, obj=None):
        # Se o usuário for superuser, pode editar todos os campos
        if request.user.is_superuser:
            return []
        
        # Para usuários normais, todos os campos são somente leitura, exceto 'status'
        return [f.name for f in self.model._meta.fields if f.name != 'status']

    def has_change_permission(self, request, obj=None):
        # Permite edição apenas do campo 'status'
        return True

    '''

    def get_enquadramentos(self, obj):
        enquads = obj.enquadramentos.all()
        return ", ".join([str(enq.enquadramento.codigo) for enq in enquads]) if enquads else "—"
    get_enquadramentos.short_description = "Enquadramento"

    

    class Media:
        js = (
            'js/mascaras.js',
        )

    @admin.action(description="Gerar Edital em DOCX")
    def gerar_edital_docx_action(self, request, queryset):
        response = gerar_edital_docx(queryset)
        queryset.update(edital_emitido=True)
        return response

    def criar_notificacao_link(self, obj):
        if obj.status != 'retido':
            return None
        if hasattr(obj, 'notificacao'):
            return "✅ Notificação emitida"

        url = reverse("admin:notificacao_notificacao_add")
        return format_html('<a class="button" href="{}?crr={}">➕ Notificar</a>', url, obj.pk)

    criar_notificacao_link.short_description = "Nova Notificação"

    



    

