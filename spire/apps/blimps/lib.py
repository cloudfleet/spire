"""Various additional functionality used by Blimp"""

import tempfile
import os
from urllib.parse import urljoin
import logging
import string
from random import sample, choice
import sys
import ssl
import base64

from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
import requests
import scrypt

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

def auth_blimp_cert(domain, request_header, certificate):
    """use certificate (or a self-signed certificate request) to
    check that the request_header contains same certificate as stored.

    """

    result = False

    try:
        client_cert_text = request_header.get("HTTP_X_PROVIDED_CERT")

        logging.debug("Client provided cert:")
        logging.debug(client_cert_text)
        logging.debug("Stored cert:")
        logging.debug(certificate)

        client_pub_key = unwrap_public_key_from_cert(client_cert_text)
        stored_pub_key = unwrap_public_key_from_cert(certificate)

        result = client_pub_key.n == stored_pub_key.n and client_pub_key.e == stored_pub_key.e
    except:
        logging.debug("Unexpected error: %s, %s, %s" % sys.exc_info())
        result = False

    return result

def unwrap_public_key_from_cert(x509_cert):
    der = ssl.PEM_cert_to_DER_cert(x509_cert)
    cert = DerSequence()
    cert.decode(der)
    tbs_certificate = DerSequence()
    tbs_certificate.decode(cert[0])
    subject_public_key_info = tbs_certificate[6]
    # Initialize RSA key
    return RSA.importKey(subject_public_key_info)

# functions recommended by the package author:
# https://bitbucket.org/mhallin/py-scrypt/src

# it seems it's implicitly latin1, while this is not resolved:
# https://bitbucket.org/mhallin/py-scrypt/issues/20/

def hash_password(password, maxtime=0.5, datalength=64):
    return base64.b64encode(scrypt.encrypt(
        generate_password(datalength), password, maxtime=maxtime
    )) # turn to string because we want to store it in the DB as a CharField

def verify_password(hashed_password, guessed_password, maxtime=0.5):
    try:
        scrypt.decrypt(base64.b64decode(hashed_password),
                       guessed_password, maxtime)
        return True
    except scrypt.error:
        return False
