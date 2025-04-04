from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notificacao


@receiver(post_save, sender=Notificacao)
def atualizar_crr_not_gerada(sender, instance, **kwargs):
    crr = instance.crr
    crr.atualizar_status_not_gerada()