"""Various additional functionality used by Blimp"""

import tempfile
import os
from urllib.parse import urljoin
import logging
import string
from random import sample, choice

import ssl
from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA

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

def auth_blimp_cert(domain, request_header, certificate):
    """use certificate (or a self-signed certificate request) to
    check that the request_header contains a signed string equal to
    domain.

    """

    client_cert_text = request_header.get("HTTP_X_PROVIDED_CERT", "nothing")

    logging.debug("Client provided cert:")
    logging.debug(client_cert_text)
    logging.debug("Stored cert:")
    logging.debug(certificate)

    client_pub_key = unwrap_public_key_from_cert(client_cert_text)
    stored_pub_key = unwrap_public_key_from_cert(certificate)

    return client_pub_key.n == stored_pub_key.n and client_pub_key.e == stored_pub_key.e

def unwrap_public_key_from_cert(x509_cert):
    der = ssl.PEM_cert_to_DER_cert(x509_cert)

    cert = DerSequence()
    cert.decode(der)
    tbs_certificate = DerSequence()
    tbs_certificate.decode(cert[0])
    subject_public_key_info = tbs_certificate[6]
    # Initialize RSA key
    return RSA.importKey(subject_public_key_info)

