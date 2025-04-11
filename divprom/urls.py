# urls.py (principal)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),  # Recomendado usar 'admin/' como prefixo
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Remova a linha do STATIC_ROOT se já estiver servindo via runserver
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)