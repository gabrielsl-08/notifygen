# urls.py (principal)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
#from crr.admin import admin_site

urlpatterns = [
    
    path('admin/', admin.site.urls),  # Recomendado usar 'admin/' como prefixo
    path('api/v1/', include('crr.api_urls')),
    path('api/v1/', include('authentication.urls')),
    
           
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Remova a linha do STATIC_ROOT se já estiver servindo via runserver
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)