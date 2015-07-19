"""Various additional functionality used by Blimp"""

import tempfile
import os
from urllib.parse import urljoin
import logging
import string
from random import sample, choice

import requests

def notify_periscope_cert_ready(blimp):
    """HTTP POST to the physical blimp's public API subset (Periscope)
    that the SSL certificate is ready to be pulled in

    """
    # create the CA_BUNDLE temp. file
    bundle_file = tempfile.TemporaryFile()
    bundle_file = tempfile.NamedTemporaryFile(delete=False)
    bundle_file.write(blimp.cert.encode())
    bundle_file.close()

    # POST away!
    r = requests.post(urljoin(blimp.url(), '/periscope/bus/certificate'),
                      json={'status': 'is_signed'},
                      verify=bundle_file.name)
    logging.debug(r.request.headers)
    logging.debug(r.request.body)
    logging.debug(r.status_code)
    logging.debug(r.json())

    # free the temp. file
    os.unlink(bundle_file.name)

def generate_password(length=255):
    chars = string.ascii_letters + string.digits
    return ''.join(choice(chars) for _ in range(length))
