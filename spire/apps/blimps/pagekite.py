import sys
from xmlrpc.client import ServerProxy
import logging

SOA = "bre.pagekite.me. 2015080100 3600 3600 7200 300"
ADMIN = 'cloudfleet.pagekite.me'
EMAIL = 'bre+%s@pagekite.net'
ACCOUNT = 'klakibre.pagekite.me'
MX = 'cloudfleet.cloudfleet.io'

# DOMAIN = 'cloudfleet-fake-test.com'
# SECRET = getpass.getpass('Password for %s: ' % ADMIN)

def error(msg):
    logging.error('{}'.format(msg))

def create_pagekite_account(domain, admin_secret):
    # This is our XML-RPC proxy object
    pks = ServerProxy('https://pagekite.net/xmlrpc/')


    # First we log in the admin account
    try:
        ok, (admin, admin_cred) = pks.login(ADMIN, admin_secret, '')
    except ValueError:
        error('Login failed')


    # Next, log-to in or create the user account
    try:
        ok, (acct, junk_cred) = pks.login(ACCOUNT, (admin, admin_cred), '')
        (a, c) = (acct, (admin, admin_cred))
    except ValueError:
        # This probably means logging in failed, try creating the account
        rc, data = pks.create_account(admin, admin_cred,
                                      EMAIL % ACCOUNT, ACCOUNT,
                                      True, False, True)  # terms, mail, activate
        if (rc != 'ok'):
            error('create_account(...%s...) failed: %s' % (ACCOUNT, rc))
        try:
            ok, (acct, acct_cred) = pks.login(ACCOUNT, (admin, admin_cred), '')
            (a, c) = (acct, (admin, admin_cred))
        except ValueError:
            error('Sub-login failed')


    # Make sure a kite exists for each of the domains we're configuring
    for dom in (domain, 'blimp.{}'.format(domain)):
        rc, data = pks.add_kite(a, c, dom, False)
        if (rc != 'ok'): error('add_kite(%s) failed: %s' % (dom, rc))

    # Configure the SOA record
    rc, data = pks.set_dns_records(a, c, domain, 'SOA', SOA)
    if (rc != 'ok'):
        error('set_dns_record(%s, SOA, ...) failed: %s' % (domain, rc))

    # Configure a TXT record
    rc, data = pks.set_dns_records(a, c, domain, 'TXT', 'Hello world')
    if (rc != 'ok'):
        error('set_dns_record(%s, TXT, ...) failed: %s' % (domain, rc))


    # # Configure a CNAME record ?
    # rc, data = pks.set_dns_records(a, c, domain, 'CNAME', 'pagekite.net')
    # if (rc != 'ok'):
    #     error('set_dns_record(%s, CNAME, ...) failed: %s' % (domain, rc))

    # Configure an MX record
    rc, data = pks.set_dns_records(a, c, domain, 'MX', MX)
    if (rc != 'ok'):
        error('set_dns_record(%s, MX, ...) failed: %s' % (domain, rc))
