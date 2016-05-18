from .base import *

#INSTALLED_APPS += ('debug_toolbar', 'django_extensions',)
INSTALLED_APPS += ('django_extensions',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bauth',
        'USER': 'postgres',
        'ADMINUSER':'postgres',
        'PASSWORD': 'Y904510P6cXM668mO96e',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}