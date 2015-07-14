"""Various additional functionality used by Blimp"""

import tempfile
import os
from urllib.parse import urljoin
import logging
import json

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
                      data=json.dumps({'status': 'is_signed'}),
                      verify=bundle_file.name)
    logging.debug(r)
    logging.debug(r.text)

    # free the temp. file
    os.unlink(bundle_file.name)
