from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',#'django.db.backends.postgresql_psycopg2',
        'NAME': 'kenblest-geodjango',
        'USER': 'postgres',
        'ADMINUSER':'postgres',
        'PASSWORD': 'C7TS*+dp~-9JHwb*7rzP',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    # ...
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': 'https://5fa65a7464454dcbadff8a7587d1eaa0:205b12d200e24b39b4c586f7df3965ba@app.getsentry.com/29978',
}