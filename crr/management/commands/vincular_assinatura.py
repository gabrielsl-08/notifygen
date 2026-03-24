from django.core.management.base import BaseCommand
from crr.models import Agente


class Command(BaseCommand):
    help = 'Vincula imagem de assinatura do S3 ao agente'

    def handle(self, *args, **options):
        agentes = {
            '80900': 'assinaturas/ass_alexandre-removebg-preview.png',
        }
        for matricula, path in agentes.items():
            try:
                a = Agente.objects.get(matricula=matricula)
                a.assinatura = path
                a.save(update_fields=['assinatura'])
                self.stdout.write(f'OK: {matricula} -> {a.assinatura.url}')
            except Agente.DoesNotExist:
                self.stdout.write(f'ERRO: agente {matricula} nao encontrado')
