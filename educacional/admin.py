from django.contrib import admin

from .models import Participante, RespostaQuestionario


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'criado_em')
    search_fields = ('nome_completo', 'email')


@admin.register(RespostaQuestionario)
class RespostaQuestionarioAdmin(admin.ModelAdmin):
    list_display = ('participante', 'pontuacao', 'total_questoes', 'percentual_acerto', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('participante__nome_completo', 'participante__email')
    readonly_fields = (
        'participante', 'respostas', 'pontuacao', 'total_questoes',
        'criticas_sugestoes', 'criado_em',
    )

    def has_add_permission(self, request):
        return False
