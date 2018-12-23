"""Various additional functionality used by Fleet"""

import logging
import string
from random import choice

from django.conf import settings
import requests

from .models import Blimp, Invite
from . import pagekite

def generate_password(length=255):
    chars = string.ascii_letters + string.digits
    return ''.join(choice(chars) for _ in range(length))

def create_pagekite_account(blimp):
    if settings.PAGEKITE_ADMIN_PASSWORD:
        logging.info('creating pagekite account using the pagekite.net API')
        pagekite.create_pagekite_account(
            blimp.domain, blimp.pagekite_secret, settings.PAGEKITE_ADMIN_PASSWORD
        )
    else:
        logging.info('no pagekite password, not notifiying API')

def update_blimp_kites(blimp, pagekite_secret, subdomains):
    if settings.PAGEKITE_ADMIN_PASSWORD:
        logging.info('updating kites for blimp')
        pagekite.update_blimp_kites(
            blimp.domain,
            pagekite_secret,
            settings.PAGEKITE_ADMIN_PASSWORD,
            subdomains
        )
    else:
        logging.info('no pagekite password, not notifiying API')


def create_blimp(domain, secret, invite_code): # TODO move to model?
    invite = Invite.objects.get(code=invite_code, used_for=None)
    blimp = Blimp(domain=domain, pagekite_secret=secret)
    blimp.save()
    invite.used_for = blimp
    invite.save()
    return blimp
