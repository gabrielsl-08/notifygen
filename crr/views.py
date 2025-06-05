from django.shortcuts import render, redirect
from .forms import (
    CrrForm, AitFormSet, VeiculoFormSet, CondutorFormSet,
    EnquadramentoFormSet, ImagemCrrFormSet
)


def criar_crr(request):
    if request.method == 'POST':
        crr_form = CrrForm(request.POST)
        veiculo_formset = VeiculoFormSet(request.POST)
        condutor_formset = CondutorFormSet(request.POST)
        ait_formset = AitFormSet(request.POST)
        enquadramento_formset = EnquadramentoFormSet(request.POST)
        imagem_formset = ImagemCrrFormSet(request.POST, request.FILES)

        if (
            crr_form.is_valid() and veiculo_formset.is_valid() and
            condutor_formset.is_valid() and ait_formset.is_valid() and
            enquadramento_formset.is_valid() and imagem_formset.is_valid()
        ):
            crr = crr_form.save(commit=False)
            crr.usuario = request.user  # opcional, se você associa o CRR ao usuário logado
            crr.save()

            # Salva os formsets vinculados ao CRR
            for formset in [
                veiculo_formset, condutor_formset, ait_formset,
                enquadramento_formset, imagem_formset
            ]:
                formset.instance = crr
                formset.save()

            return redirect('listar_crr')  # ajuste conforme o nome real da sua URL

    else:
        crr_form = CrrForm()
        veiculo_formset = VeiculoFormSet()
        condutor_formset = CondutorFormSet()
        ait_formset = AitFormSet()
        enquadramento_formset = EnquadramentoFormSet()
        imagem_formset = ImagemCrrFormSet()

    return render(request, 'crr/crr_form.html', {
        'crr_form': crr_form,
        'veiculo_formset': veiculo_formset,
        'condutor_formset': condutor_formset,
        'ait_formset': ait_formset,
        'enquadramento_formset': enquadramento_formset,
        'imagem_formset': imagem_formset,
    })

