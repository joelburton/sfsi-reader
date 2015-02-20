"""Common settings and globals."""


from os.path import abspath, basename, dirname, join, normpath
from sys import path


DJANGO_ROOT = dirname(dirname(abspath(__file__)))    # project directory
SITE_ROOT = dirname(DJANGO_ROOT)                     # project folder
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Joel Burton', 'joel@joelburton.com'),
)
MANAGERS = ADMINS


TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

SITE_ID = 1


MEDIA_ROOT = normpath(join(SITE_ROOT, '..', 'media'))
MEDIA_URL = '/media/'


STATIC_ROOT = normpath(join(SITE_ROOT, '..', 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (normpath(join(SITE_ROOT, 'static')),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


SECRET_KEY = r"+8n*=7j@+^pkbwwjo%83#i6*f2n98p5e!0_g6!x_pt$5jo9&q&"


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'resources.context_processors.site_nav',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (normpath(join(SITE_ROOT, 'templates')),)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = '%s.urls' % SITE_NAME


DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin panel and documentation:
    'grappelli',
    'django.contrib.admin',

    'bootstrap3',
    'django_comments',
    'avatar',
    'django_extensions',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'resources',
    'members',
    'bookmarks',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

GRAPPELLI_ADMIN_TITLE = 'SFSI Reader Administration'


########### ALL AUTH CONFIGURATION

TEMPLATE_CONTEXT_PROCESSORS += (
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
)

BOOTSTRAP3 = {
    'css_url': "//netdna.bootstrapcdn.com/bootswatch/3.3.2/yeti/bootstrap.min.css"
}


# Joel's MacBook can timeout when at a cafe with incorrectly-set DNS settings, as it doesn't know
# the hostname of the laptop. So let's hack this in:

from django.core.mail.utils import DNS_NAME

DNS_NAME._fqdn = "localhost"



MIDDLEWARE_CLASSES += (
    'reader.middleware.LoginRequiredMiddleware',
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# We require that account have an email and it must be verified before they can use our site
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# We have a custom user model and therefore a custom registration form
AUTH_USER_MODEL = "members.Member"
# ACCOUNT_SIGNUP_FORM_CLASS = "members.forms.MemberRegistrationForm"

# If users use the "remember me" feature, so they stay logged in after they close their browser,
# we keep their session around for 2 weeks
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

LOGIN_REDIRECT_URL = '/'


##################################################################################################
# User avatars
#
# We use django-avatar for this. We fall back to using Gravatar and have a Gravatar fallback, of
# our grey-user icon.

AVATAR_STORAGE_DIR = "avatars"
AVATAR_GRAVATAR_DEFAULT = "mm"
AUTO_GENERATE_AVATAR_SIZES = (20, 250,)

LOGIN_EXEMPT_URLS = ["accounts/password/reset/"]

LOGGING = {
    'version': 1,

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
