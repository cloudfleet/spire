"""
Django settings for spire project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from sys import platform as _platform
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b=-s+lqg2ghsgm9ikw)3+sv3bx-!tc6tr%h9cv4!%&7-2o%nt$'

# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    'bootstrapform',
    'rest_framework',
    'corsheaders',
    'djangosecure',
    'spire.apps.blimps',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spire.middleware.RequireLoginMiddleware',
)

ROOT_URLCONF = 'spire.urls'

WSGI_APPLICATION = 'spire.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Parse database configuration from $DATABASE_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if 'DATABASE_URL' in os.environ: # production environment
    DEPLOYMENT = 'production'
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['*']
    # DB config
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # email config
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST= 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']

    # add extra apps
    #INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)

    BROKER_URL = os.environ["BROKER_URL"]


else: # development environment
    DEPLOYMENT = 'development'
    DEBUG = True
    TEMPLATE_DEBUG = True
    # print e-mails to the console instead of sending them
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    import sys
    if 'manage' in sys.argv[0]:
        INSTALLED_APPS += ('django_extensions',
                           'debug_toolbar.apps.DebugToolbarConfig', )
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INTERNAL_IPS = ('127.0.0.1', )
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    # end django-debug-toolbar

    CELERY_ALWAYS_EAGER = True # run tasks in same thread for development
    #CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    MEDIA_URL = '/media/'
# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    # allauth specific context processors
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth' specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'static'),
)

# User registration


SITE_ID = 1

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7 # after this period, the account gets locked

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # or 'optional' or 'none'

# who to notify with admin e-mails
ADMINS = (('admin', 'admin@localhost'), )
# shown in the "from" field of e-mails by default
DEFAULT_FROM_EMAIL = ADMINS[0][1]

# login_required urls

LOGIN_REQUIRED_URLS = (
    r'/dashboard/(.*)$',
)

# TODO: better separation of API and other urls
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/dashboard/blimp/api/(.*)$',
)

# Celery
#CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

# Django REST framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# CORS settings
# CORS_ORIGIN_ALLOW_ALL = True # (False by default)
CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)?(\w+\.)?cloudfleet\.io$',
    '^(http://)localhost:?(\d+)?$' # for development
)
CORS_URLS_REGEX = r'^/api/.*$' # (^.*$' by default)


# CloudFleet-specific settings
#-----------------------------

# whether or not Spire should automatically start blimp containers
SPIRE_CONTROL_BLIMPYARD = True

# the host and port on Spire to bind the Blimpyard Docker API
SPIRE_DOCKER_API_HOST = 'localhost'
SPIRE_DOCKER_API_PORT = 4444
# test tunneling worked with this during ordering:
# curl -X GET http://localhost:4444/images/json

# DOCKER API port
DOCKER_PORT = 4243
# the image to build the container from
DOCKER_IMAGE = 'cloudfleet/blimp'

# path to the private ssh used to connect to blimpyard (docker, pagekite)
if DEPLOYMENT == 'development':
    SPIRE_CONTROL_BLIMPYARD = False
    BLIMPYARD_KEY = None
    BLIMPYARD_URL = 'localhost'
    BLIMPYARD_USER = None
    BLIMPYARD_PAGEKITE_PORT = 60666
    if _platform == "darwin":
        # TODO: solve for OS X - see boot2docker info
        DOCKER_PORT = 2375
        BLIMPYARD_KEY = '~/.ssh/id_boot2docker'
        BLIMPYARD_URL = '192.168.59.103'
        BLIMPYARD_USER = 'docker'
elif DEPLOYMENT == 'production':
    BLIMPYARD_KEY = '~/.ssh/blimpyard_rsa'
    BLIMPYARD_URL = 'blimpyard.cloudfleet.io'
    BLIMPYARD_USER = 'kermit'
    BLIMPYARD_PAGEKITE_PORT = 80

# the base domain and port through which the blimps can be accessed
BLIMP_DOMAIN = BLIMPYARD_URL
BLIMP_SUBDOMAIN = 'blimp'
BLIMP_PORT = BLIMPYARD_PAGEKITE_PORT

# logging configuration
import logging
import logstash

LOG_PATH, LOG_FILENAME = '.', 'spire.log'
LOG_LEVEL = logging.DEBUG
LOG_MAX = 10**6 # bytes
LOGSTASH_HOST, LOGSTASH_PORT = 'localhost', 5959

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            os.path.join(LOG_PATH, LOG_FILENAME), maxBytes=LOG_MAX
        ), # file output
        logging.StreamHandler(), # stdout
        logstash.LogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, version=1)
    ]
)

# TODO: Django logging settings:
# https://pypi.python.org/pypi/python-logstash/0.3.1

# to override these settings, create local_settings.py and run as
#     ./manage.py --settings=local_settings runserver
