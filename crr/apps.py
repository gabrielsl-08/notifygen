from django.apps import AppConfig


class CrrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crr'

def ready(self):
    import crr.signals  # ou o nome correto do módulo