from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from crr.models import Crr
from django.forms import modelform_factory
from crr.models import Crr

CrrForm = modelform_factory(Crr, exclude=['usuario'])

@login_required
def criar_crr(request):
    if request.method == 'POST':
        form = CrrForm(request.POST, request.FILES)
        if form.is_valid():
            crr = form.save(commit=False)
            crr.usuario = request.user  # Supondo que você adicione esse campo na model
            crr.save()
            return redirect('mobile:lista_crr')
    else:
        form = CrrForm()
    return render(request, 'mobile/criar_crr.html', {'form': form})

@login_required
def lista_crr(request):
    crrs = Crr.objects.filter(usuario=request.user)
    return render(request, 'mobile/lista_crr.html', {'crrs': crrs})

@login_required
def imprimir_crr(request, pk):
    crr = get_object_or_404(Crr, pk=pk, usuario=request.user)
    # Aqui você pode usar a lógica de geração de PDF ou visualização
    return render(request, 'mobile/imprimir_crr.html', {'crr': crr})
