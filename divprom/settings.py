from pathlib import Path
import os  
import dj_database_url
import environ




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env") 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env("DEBUG")

#ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
ALLOWED_HOSTS = ['*']




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Alternativa moderna: BASE_DIR / 'media'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework_simplejwt.authentication.JWTAuthentication',
         ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',

    ## Rate limiting para usuários anônimos     
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Máximo 100 requisições por hora para usuários anônimos
        'user': '1000/hour'  # Mais permissivo para usuários autenticados
    }

     }

# Permissão para POST, PUT, DELETE
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000','https://divprom.herokuapp.com']  # ajuste se necessário
CSRF_COOKIE_HTTPONLY = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'divprom.urls'


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crr',
    'notificacao',
    'import_export',
    'rest_framework',
    'rest_framework_simplejwt',
    'authentication',
    "bootstrap5",

]

# Configuração do Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "DIVPROM",
    "site_header": "DIVPROM",
    "site_brand": "DIVPROM",
    "welcome_sign": "Bem-vindo ao Sistema DIVPROM",
    "copyright": "Prefeitura Municipal de São Sebastião",
    "search_model": ["crr.Crr"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "crr.Crr": "fas fa-file-alt",
        "crr.TabelaEnquadramento": "fas fa-table",
        "crr.TabelaArrendatario": "fas fa-building",
        "notificacao.Notificacao": "fas fa-envelope",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "use_google_fonts_cdn": True,
    "changeform_format": "vertical_tabs",
    "changeform_format_overrides": {
        "crr.crr": "vertical_tabs",
    },
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'crr' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'divprom.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Formatação de datas
DATE_INPUT_FORMATS = ['%d/%m/%Y']
TIME_INPUT_FORMATS = ['%H:%M']
SHORT_DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i'

# Autenticação: usar login do Django Admin
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/crr/'










