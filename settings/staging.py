from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cards_web',
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
    # 'debug_toolbar',
    'django_extensions',
)

## uncommet the following and add the dsn matching your project
# RAVEN_CONFIG = {
#     'dsn': 'https://5fa65a7464454dcbadff8a7587d1eaa0:205b12d200e24b39b4c586f7df3965ba@app.getsentry.com/29978',
# }

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'