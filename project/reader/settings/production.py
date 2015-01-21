"""Production settings and globals."""

from __future__ import absolute_import

from os import environ

from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'reader.joelburton.com', 'reader.sfsi.org']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'joel@joelburton.com')
EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reader',
        'USER': 'reader',
        'PASSWORD': environ.get('PG_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5433',
        'CONN_MAX_AGE': None,
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY')

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
