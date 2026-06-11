from django.db import models


class Participante(models.Model):
    nome_completo = models.CharField('Nome completo', max_length=200)
    email = models.EmailField('E-mail')
    criado_em = models.DateTimeField('Data de cadastro', auto_now_add=True)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.nome_completo} ({self.email})'


class RespostaQuestionario(models.Model):
    participante = models.ForeignKey(
        Participante, on_delete=models.CASCADE, related_name='respostas_questionario'
    )
    respostas = models.JSONField('Respostas', help_text='Mapa {numero_questao: alternativa}')
    pontuacao = models.PositiveSmallIntegerField('Pontuação')
    total_questoes = models.PositiveSmallIntegerField('Total de questões')
    criticas_sugestoes = models.TextField('Críticas e sugestões', blank=True)
    criado_em = models.DateTimeField('Respondido em', auto_now_add=True)

    class Meta:
        verbose_name = 'Resposta de questionário'
        verbose_name_plural = 'Respostas de questionários'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.participante.nome_completo} - {self.pontuacao}/{self.total_questoes}'

    @property
    def percentual_acerto(self):
        if not self.total_questoes:
            return 0
        return round((self.pontuacao / self.total_questoes) * 100, 1)
