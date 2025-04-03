from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path


from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', admin.site.urls),
    
]
####### DEVE SER CONFIGURADO O SERVIDOR DE ARQUIVOS STATICOS ##########
# Isso só deve ser adicionado em desenvolvimento (DEBUG=True)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]