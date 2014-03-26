"""
WSGI config for spire project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spire.settings")

# Run startup code! - moved to the blimps model using bgtunnel
#import subprocess
#cmd = 'ssh -o BatchMode=yes -i ~/.ssh/blimpyard_rsa -f -N -L 4444:localhost:4243 kermit@blimpyard.cloudfleet.io'
#process = subprocess.Popen(cmd.split())#, stdout=subprocess.PIPE)
import logging
logging.info('\n-------------\nSpire started\n-------------')

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
