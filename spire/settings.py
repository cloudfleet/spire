"""
Django settings for spire project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b=-s+lqg2ghsgm9ikw)3+sv3bx-!tc6tr%h9cv4!%&7-2o%nt$'


# Application definition

INSTALLED_APPS = (
    'djcelery',
    'registration_defaults',
    'registration',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.sites', TODO: enable, registration recommends it
    'south',
    'spire.apps.blimps',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
    INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)
else: # development environment
    DEBUG = True
    TEMPLATE_DEBUG = True
    # print e-mails to the console instead of sending them
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
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

from registration_defaults.settings import *

ACCOUNT_ACTIVATION_DAYS = 7 # after this period, the account gets locked

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# login_required urls

LOGIN_REQUIRED_URLS = (
    r'/dashboard/(.*)$',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = ()

# Celery
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
#CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


# Cloudfleet-specific settings
#-----------------------------

# path to the private ssh used to connect to blimpyard (docker, pagekite)
BLIMPYARD_KEY = '~/.ssh/blimpyard_rsa'
BLIMPYARD_URL = 'blimpyard.cloudfleet.io'
BLIMPYARD_USER = 'kermit'
DOCKER_PORT = 4243
DOCKER_IMAGE = 'cloudfleet/simple-ldap' # the image to build the container from
