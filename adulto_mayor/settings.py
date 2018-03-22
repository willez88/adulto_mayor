"""
Django settings for adulto_mayor project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'egl3(s$w#!-*g#+#)*bn-wk3x%pnq42t^@kt5-o^((q40#xm5l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

## Identifica a los administradores del sistema
ADMINS = [
    ('William Páez', 'wpaez@cenditel.gob.ve'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'base',
    'usuario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adulto_mayor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'adulto_mayor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adulto_mayor',
        'USER': 'admin',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'inicio'

LOGOUT_REDIRECT_URL = 'login'

#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
EMAIL_HOST_USER = 'correo@gmail.com'
#EMAIL_HOST_PASSWORD = 'clave'
EMAIL_FROM = EMAIL_HOST_USER
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

## Registro de mensajes al usuario
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

## Registro de vitácoras de errores (logs)
LOGS_PATH = ''

## Configuración de los niveles de vitácoras (logs) a registrar
LOGGING = dict(version=1, disable_existing_loggers=True, formatters={
    'std': {
        'format': '%(asctime)s %(levelname)-8s [modulo: %(module)s, funcion: %(funcName)s, linea: %(lineno)d]. %(message)s',
    }
}, handlers={
    'null': {
        'level': 'DEBUG',
        'class': 'logging.NullHandler'
    },
    'base': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'base.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
    'usuario': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'usuario.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
}, loggers={
    'root': {
        'level': 'DEBUG',
        'handlers': ['usuario']
    },
    'base': {
        'level': 'DEBUG',
        'handlers': ['base'],
        'qualname': 'base'
    },
    'usuario': {
        'level': 'DEBUG',
        'handlers': ['usuario'],
        'qualname': 'usuario'
    },
    'django.request': {
        'handlers': ['null'],
        'level': 'ERROR',
        'propagate': False,
    }
})
