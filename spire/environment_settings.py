from .settings import *
import os

# general settings
#=================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '', # Set to empty string for default.
    }
}

# Administrators
ADMINS = (('Admiralty', 'admiralty@cloudfleet.io'), )
# shown in the "from" field of e-mails by default
DEFAULT_FROM_EMAIL = ADMINS[0][1]

# media
MEDIA_ROOT = '/opt/media/'
MEDIA_URL = '/media/'
