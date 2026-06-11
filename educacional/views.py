from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import QuestionarioForm
from .models import Participante, RespostaQuestionario
from .questoes import QUESTOES, get_gabarito


def quiz_view(request):
    if request.method == 'POST':
        form = QuestionarioForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            gabarito = get_gabarito()

            respostas = {}
            pontuacao = 0
            for questao in QUESTOES:
                qid = str(questao['id'])
                resposta = cd[f'questao_{qid}']
                respostas[qid] = resposta
                if resposta == gabarito[qid]:
                    pontuacao += 1

            participante, criado = Participante.objects.get_or_create(
                email=cd['email'],
                defaults={'nome_completo': cd['nome_completo']},
            )
            if not criado and participante.nome_completo != cd['nome_completo']:
                participante.nome_completo = cd['nome_completo']
                participante.save(update_fields=['nome_completo'])

            resposta_obj = RespostaQuestionario.objects.create(
                participante=participante,
                respostas=respostas,
                pontuacao=pontuacao,
                total_questoes=len(QUESTOES),
                criticas_sugestoes=cd.get('criticas_sugestoes', ''),
            )
            return redirect('educacional:resultado', pk=resposta_obj.pk)
    else:
        form = QuestionarioForm()

    return render(request, 'educacional/quiz.html', {'form': form})


def resultado_view(request, pk):
    resposta_obj = get_object_or_404(RespostaQuestionario, pk=pk)
    gabarito = get_gabarito()

    detalhes = []
    for questao in QUESTOES:
        qid = str(questao['id'])
        resposta_marcada = resposta_obj.respostas.get(qid)
        correta = gabarito[qid]
        detalhes.append({
            'questao': questao,
            'resposta_marcada': resposta_marcada,
            'texto_marcado': questao['alternativas'].get(resposta_marcada, '—'),
            'texto_correto': questao['alternativas'][correta],
            'correta': correta,
            'acertou': resposta_marcada == correta,
        })

    return render(request, 'educacional/resultado.html', {
        'resposta_obj': resposta_obj,
        'detalhes': detalhes,
    })


@login_required
def estatisticas_view(request):
    respostas_qs = RespostaQuestionario.objects.select_related('participante').all()
    total_participantes = respostas_qs.count()
    total_questoes = len(QUESTOES)

    media_pontuacao = respostas_qs.aggregate(media=Avg('pontuacao'))['media'] or 0
    media_percentual = (media_pontuacao / total_questoes * 100) if total_questoes else 0

    gabarito = get_gabarito()
    estatisticas_questoes = []
    for questao in QUESTOES:
        qid = str(questao['id'])
        correta = gabarito[qid]
        acertos = sum(1 for r in respostas_qs if r.respostas.get(qid) == correta)
        percentual = (acertos / total_participantes * 100) if total_participantes else 0
        estatisticas_questoes.append({
            'questao': questao,
            'acertos': acertos,
            'percentual': round(percentual, 1),
        })

    distribuicao = {'0-3': 0, '4-6': 0, '7-8': 0, '9-10': 0}
    for r in respostas_qs:
        if r.pontuacao <= 3:
            distribuicao['0-3'] += 1
        elif r.pontuacao <= 6:
            distribuicao['4-6'] += 1
        elif r.pontuacao <= 8:
            distribuicao['7-8'] += 1
        else:
            distribuicao['9-10'] += 1

    agora = timezone.now()
    participantes_7d = respostas_qs.filter(criado_em__gte=agora - timedelta(days=7)).count()
    participantes_30d = respostas_qs.filter(criado_em__gte=agora - timedelta(days=30)).count()

    return render(request, 'educacional/estatisticas.html', {
        'total_participantes': total_participantes,
        'media_pontuacao': round(media_pontuacao, 2),
        'media_percentual': round(media_percentual, 1),
        'total_questoes': total_questoes,
        'estatisticas_questoes': sorted(estatisticas_questoes, key=lambda item: item['percentual']),
        'distribuicao': distribuicao,
        'participantes_7d': participantes_7d,
        'participantes_30d': participantes_30d,
        'ultimas_respostas': respostas_qs[:10],
    })
