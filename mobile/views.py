from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from crr.models import Crr
from .forms import CrrForm
from .utils import gerar_proximo_numero_crr
from django.core.files.base import ContentFile
import base64
from django.http import HttpResponse

@login_required
def criar_crr_mobile(request):
    crr_saved = None
    if request.method == 'POST':
        form = CrrForm(request.POST)
        if form.is_valid():
            crr = form.save(commit=False)
            signature_data = request.POST.get('signature', None)
            if signature_data:
                format, imgstr = signature_data.split(';base64,')
                ext = format.split('/')[-1]
                crr.signature.save(f'signature.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
            crr.save()
            crr_saved = crr  # Adiciona o CRR salvo à flag
            form = CrrForm()  # Reseta o formulário após salvamento
    else:
        form = CrrForm()
    
    return render(request, 'mobile/criar_crr.html', {'form': form, 'crr_saved': crr_saved})




@login_required
def lista_crrs(request):
    crrs = Crr.objects.filter(usuario=request.user)
    return render(request, 'mobile/lista.html', {'crrs': crrs})

def imprimir_crr(request, crr_id):
    crr = get_object_or_404(Crr, id=crr_id)
    return render(request, 'mobile/imprimir_crr.html', {'crr': crr})