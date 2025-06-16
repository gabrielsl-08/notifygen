from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Crr, Veiculo, Condutor, Ait, Enquadramento, ImagemCrr,Arrendatario
from notificacao.models import LogGeracaoEdital
from .forms import (   CrrForm, VeiculoForm, CondutorForm, AitForm, EnquadramentoForm, ImagemCrrForm,ArrendatarioForm)
from .forms import VeiculoFormSet, CondutorFormSet, AitFormSet,EnquadramentoFormSet,ImagemCrrFormSet, ArrendatarioFormSet
from notificacao.admin import gerar_pdf_notificacoes
from django.contrib.auth.decorators import login_required
from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .utils import gerar_edital_docx
from django.db.models import Prefetch # Importe Prefetch
import logging
logger = logging.getLogger(__name__)
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .choices import STATUS_CHOICES

@require_POST
def alterar_status_crr(request):
    if request.method == "POST":
        crr_id = request.POST.get("crr_id")
        novo_status = request.POST.get("novo_status")

        if novo_status in dict(STATUS_CHOICES).keys():  # usa o importado
            try:
                crr = Crr.objects.get(id=crr_id)
                crr.status = novo_status
                crr.save()
                messages.success(request, "Status atualizado com sucesso.")
            except Crr.DoesNotExist:
                messages.error(request, "CRR não encontrado.")
        else:
            messages.error(request, "Status inválido.")

    return redirect('listar_crr')

@login_required
def gerar_edital_view(request):
    if request.method == 'POST':
        crr_ids = request.POST.getlist('crr_ids')

        if not crr_ids:
            messages.error(request, "Por favor, selecione ao menos um CRR para gerar o edital.")
            return redirect(request.META.get('HTTP_REFERER', 'listar_crr'))

        crrs_para_processar = Crr.objects.filter(
            id__in=crr_ids,
            status='retido',
            edital_emitido=False
        ).prefetch_related(
            'veiculo',
            'notificacao',
            Prefetch('arrendatarios', queryset=Arrendatario.objects.select_related('arrendatario'))
        )

        if not crrs_para_processar.exists():
            messages.error(request, "Nenhum dos CRRs selecionados está elegível para geração de edital (Status não é 'Retido' ou Edital já emitido), ou não foram encontrados.")
            return redirect(request.META.get('HTTP_REFERER', 'listar_crr'))

        try:
            num_crrs_processados = crrs_para_processar.count()
            response = gerar_edital_docx(crrs_para_processar)

            crrs_para_processar.update(edital_emitido=True)

            # 🟢 GERAÇÃO DO LOG DE EDITAL
            numero_edital = f"EDT-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            LogGeracaoEdital.objects.create(
                numero_edital=numero_edital,
                usuario=request.user,
                crrs_gerados=", ".join([crr.numeroCrr for crr in crrs_para_processar])
            )

            messages.success(request, f"Edital gerado com sucesso para {num_crrs_processados} CRR(s).")
            return response

        except FileNotFoundError as e:
            logger.error(f"Erro ao carregar template DOCX: {e}")
            messages.error(request, f"Erro ao gerar o edital: Template do documento não encontrado ou inválido. Detalhes: {e}")
            return redirect(request.META.get('HTTP_REFERER', 'listar_crr'))

        except Exception as e:
            logger.exception("Erro inesperado durante a geração de edital na view:")
            messages.error(request, f"Ocorreu um erro interno ao gerar o edital. Detalhes: {str(e)}")
            return redirect(request.META.get('HTTP_REFERER', 'listar_crr'))

    return HttpResponseBadRequest("Requisição inválida ou método não permitido.")


def aplicar_filtros_crr(queryset, filtro_nome=None, termo_busca=None):
    # Filtro por status especial
    if filtro_nome == 'atrasado':
        data_limite = date.today() - timedelta(days=10)
        queryset = queryset.filter(dataFiscalizacao__lte=data_limite, not_gerada=False, status='retido')
    elif filtro_nome == 'edital':
        data_limite = date.today() - timedelta(days=30)
        queryset = queryset.filter(dataFiscalizacao__lte=data_limite, edital_emitido=False, status='retido')

    # Filtro por termo de busca (número ou placa)
    if termo_busca:
        queryset = queryset.filter(
            Q(numeroCrr__icontains=termo_busca) | Q(veiculo__placa__icontains=termo_busca)
        )

    return queryset

def gerar_pdf_crr(request, pk):
    return gerar_pdf_notificacoes(request, pk)



@login_required
def listar_crr(request):
    filtro_nome = request.GET.get('crr_filtro')
    termo_busca = request.GET.get('q')  # parâmetro de busca

    crrs = Crr.objects.filter(status__in=['retido', 'liberado']).order_by('-dataFiscalizacao')
    crrs = aplicar_filtros_crr(crrs, filtro_nome, termo_busca)

    if request.method == 'POST':
        crr_id = request.POST.get('crr_id')
        novo_status = request.POST.get('novo_status')
        crr = get_object_or_404(Crr, id=crr_id)

        if request.user.is_superuser or novo_status == 'liberado':
            crr.status = novo_status
            crr.save()
        return redirect('listar_crr')

    admin_context = site.each_context(request)
    context = {
        'crrs': crrs,
        'status_choices': Crr._meta.get_field('status').choices,
        'filtro_aplicado': filtro_nome,
        'termo_busca': termo_busca,
        'title': 'Lista de CRRs',
        'site_title': 'Sistema CRR',
        'site_header': 'Administração do Sistema CRR',
        **admin_context,
    }
    return render(request, 'crr/listar_crr.html', context)

@login_required
def detalhar_crr(request, pk):
    crr = get_object_or_404(Crr, pk=pk)

    # Instancia os formulários e formsets normalmente
    crr_form = CrrForm(instance=crr)
    veiculo_formset = VeiculoFormSet(instance=crr)
    condutor_formset = CondutorFormSet(instance=crr)
    ait_formset = AitFormSet(instance=crr)
    enquadramento_formset = EnquadramentoFormSet(instance=crr)
    imagem_formset = ImagemCrrFormSet(instance=crr)

    # Torna todos os campos do formulário principal desabilitados
    for field in crr_form.fields.values():
        field.disabled = True

    # Torna todos os campos dos formsets desabilitados
    for formset in [veiculo_formset, condutor_formset, ait_formset, enquadramento_formset, imagem_formset]:
        for form in formset:
            for field in form.fields.values():
                field.disabled = True

    context = {
        'crr': crr,
        'crr_form': crr_form,
        'veiculo_formset': veiculo_formset,
        'condutor_formset': condutor_formset,
        'ait_formset': ait_formset,
        'enquadramento_formset': enquadramento_formset,
        'imagem_formset': imagem_formset,
    }

    return render(request, 'crr/detalhar_crr.html', context)
'''
@login_required
def detalhar_crr(request, pk):
    """Exibe detalhes de um CRR específico"""
    crr = get_object_or_404(Crr, pk=pk)
    veiculo = Veiculo.objects.filter(crr=crr).first()
    condutor = Condutor.objects.filter(crr=crr).first()
    aits = Ait.objects.filter(crr=crr)
    enquadramentos = Enquadramento.objects.filter(crr=crr)
    imagens = ImagemCrr.objects.filter(crr=crr)
    
    # Contexto do admin para manter o menu lateral
    admin_context = site.each_context(request)
    
    context = {
        'crr': crr,
        'veiculo': veiculo,
        'condutor': condutor,
        'aits': aits,
        'enquadramentos': enquadramentos,
        'imagens': imagens,
        'title': f'CRR #{crr.numeroCrr}',
        'site_title': 'Sistema CRR',
        'site_header': 'Administração do Sistema CRR',
        **admin_context,
    }
    
    return render(request, 'crr/detalhar_crr.html', context)
'''
@login_required  # ou @login_required se todos usuários logados puderem acessar
def triagem_crr(request):
    crrs_pendentes = Crr.objects.filter(status='pendente').order_by('-dataFiscalizacao')
    admin_context = site.each_context(request)
    context = {
        'crr_list': crrs_pendentes,
        'title': 'Triagem de CRRs Pendentes',
        'site_title': 'Sistema CRR',
        'site_header': 'Administração do Sistema CRR',
        **admin_context,
    }
    return render(request, 'crr/triagem_crr.html', context)

from django.forms import modelformset_factory
from .forms import AitForm

@staff_member_required
def revisar_crr(request, pk):
    crr = get_object_or_404(Crr, pk=pk)

    AitFormSet = modelformset_factory(Ait, form=AitForm, extra=0, can_delete=False)
    EnquadramentoFormSet = modelformset_factory(Enquadramento, form=EnquadramentoForm, extra=0, can_delete=False)
    ImagemCrrFormSet = modelformset_factory(ImagemCrr, form=ImagemCrrForm, extra=0, can_delete=False)

    if request.method == 'POST':
        form = CrrForm(request.POST, request.FILES, instance=crr)
        veiculo_form = VeiculoForm(request.POST, request.FILES, instance=crr.veiculo.first())
        arrendatario_form = ArrendatarioForm(request.POST, instance=crr.arrendatario)

        ait_formset = AitFormSet(request.POST, queryset=Ait.objects.filter(crr=crr), prefix='ait')
        enquadramento_formset = EnquadramentoFormSet(request.POST, queryset=Enquadramento.objects.filter(crr=crr), prefix='enq')
        imagem_formset = ImagemCrrFormSet(request.POST, request.FILES, queryset=ImagemCrr.objects.filter(crr=crr), prefix='img')

        if (
            form.is_valid() and veiculo_form.is_valid() and arrendatario_form.is_valid()
            and ait_formset.is_valid() and enquadramento_formset.is_valid() and imagem_formset.is_valid()
        ):
            crr = form.save(commit=False)
            crr.status = 'retido'
            crr.save()

            veiculo = veiculo_form.save(commit=False)
            veiculo.crr = crr
            veiculo.save()

            arrendatario = arrendatario_form.save(commit=False)
            arrendatario.crr = crr
            arrendatario.save()
            

            ait_formset.save()
            enquadramento_formset.save()
            imagem_formset.save()

            return redirect('triagem_crr')
    else:
        form = CrrForm(instance=crr)
        veiculo_form = VeiculoForm(instance=crr.veiculo.first())
        arrendatario = Arrendatario.objects.filter(crr=crr).first()
        arrendatario_form = ArrendatarioForm(instance=arrendatario)
        ait_formset = AitFormSet(queryset=Ait.objects.filter(crr=crr), prefix='ait')
        enquadramento_formset = EnquadramentoFormSet(queryset=Enquadramento.objects.filter(crr=crr), prefix='enq')
        imagem_formset = ImagemCrrFormSet(queryset=ImagemCrr.objects.filter(crr=crr), prefix='img')

    context = {
        'form': form,
        'veiculo_form': veiculo_form,
        'arrendatario_form': arrendatario_form,
        'ait_formset': ait_formset,
        'enquadramento_formset': enquadramento_formset,
        'imagem_formset': imagem_formset,
        'title': f'Revisar CRR #{crr.numeroCrr}',
        **site.each_context(request),
    }

    return render(request, 'crr/revisar_crr.html', context)



@login_required
def criar_crr(request):
    """Cria um novo CRR"""
    AitFormSet = modelformset_factory(Ait, form=AitForm, extra=0, can_delete=True)
    EnquadramentoFormSet = modelformset_factory(Enquadramento, form=EnquadramentoForm, extra=0, can_delete=True)
    ImagemCrrFormSet = modelformset_factory(ImagemCrr, form=ImagemCrrForm, extra=0, can_delete=True)
    
    if request.method == 'POST':
        crr_form = CrrForm(request.POST)
        veiculo_form = VeiculoForm(request.POST, request.FILES)
        condutor_form = CondutorForm(request.POST, request.FILES)
        ait_formset = AitFormSet(request.POST, request.FILES, prefix='ait')
        enquadramento_formset = EnquadramentoFormSet(request.POST, request.FILES, prefix='enquadramento')
        imagem_formset = ImagemCrrFormSet(request.POST, request.FILES, prefix='imagem')
        
        if (
            crr_form.is_valid() and
            veiculo_form.is_valid() and
            condutor_form.is_valid() and
            ait_formset.is_valid() and
            enquadramento_formset.is_valid() and
            imagem_formset.is_valid()
        ):
            crr = crr_form.save()
            
            veiculo = veiculo_form.save(commit=False)
            veiculo.crr = crr
            veiculo.save()
            
            condutor = condutor_form.save(commit=False)
            condutor.crr = crr
            condutor.save()
            
            for form in ait_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    obj = form.save(commit=False)
                    obj.crr = crr
                    obj.save()
            
            for form in enquadramento_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    obj = form.save(commit=False)
                    obj.crr = crr
                    obj.save()
            
            for form in imagem_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    obj = form.save(commit=False)
                    obj.crr = crr
                    obj.save()
            
            messages.success(request, f'CRR #{crr.numero_crr} criado com sucesso!')
            return redirect('listar_crr')
        else:
            messages.error(request, 'Erro ao salvar o CRR. Verifique os dados informados.')
    else:
        crr_form = CrrForm()
        veiculo_form = VeiculoForm()
        condutor_form = CondutorForm()
        ait_formset = AitFormSet(queryset=Ait.objects.none(), prefix='ait')
        enquadramento_formset = EnquadramentoFormSet(queryset=Enquadramento.objects.none(), prefix='enquadramento')
        imagem_formset = ImagemCrrFormSet(queryset=ImagemCrr.objects.none(), prefix='imagem')
    
    # Contexto do admin para manter o menu lateral
    admin_context = site.each_context(request)
    
    context = {
        'crr_form': crr_form,
        'veiculo_form': veiculo_form,
        'condutor_form': condutor_form,
        'ait_formset': ait_formset,
        'enquadramento_formset': enquadramento_formset,
        'imagem_formset': imagem_formset,
        'title': 'Criar Novo CRR',
        'site_title': 'Sistema CRR',
        'site_header': 'Administração do Sistema CRR',
        **admin_context,
    }
    
    return render(request, 'crr/crr_form.html', context)
