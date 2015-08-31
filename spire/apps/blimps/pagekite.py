import sys
from xmlrpc.client import ServerProxy
import logging

ADMIN = 'cloudfleet.pagekite.me'
MX = 'cloudfleet.cloudfleet.io'

# SOA = "bre.pagekite.me. 2015080100 3600 3600 7200 300"
# EMAIL = 'bre+%s@pagekite.net'
# ACCOUNT = 'klakibre.pagekite.me'
# DOMAIN = 'cloudfleet-fake-test.com'
# SECRET = getpass.getpass('Password for %s: ' % ADMIN)

def error(msg):
    logging.error('{}'.format(msg))

def create_pagekite_account(domain, domain_secret, admin_secret):
    # This is our XML-RPC proxy object
    pks = ServerProxy('https://pagekite.net/xmlrpc/')

    # create some hopefully unique account name
    account = domain.replace('.', '-') + '.myblimp.net'
    email = 'user+%s@myblimp.net'

    # First we log in the admin account
    try:
        ok, (admin, admin_cred) = pks.login(ADMIN, admin_secret, '')
    except ValueError:
        error('Login failed')


    # Next, log-to in or create the user account
    try:
        ok, (acct, junk_cred) = pks.login(account, (admin, admin_cred), '')
        (a, c) = (acct, (admin, admin_cred))
    except ValueError:
        # This probably means logging in failed, try creating the account
        rc, data = pks.create_account(admin, admin_cred,
                                      email % account, account,
                                      True, False, True)  # terms, mail, activate
        if (rc != 'ok'):
            error('create_account(...%s...) failed: %s' % (account, rc))
        try:
            ok, (acct, acct_cred) = pks.login(account, (admin, admin_cred), '')
            (a, c) = (acct, (admin, admin_cred))
        except ValueError:
            error('Sub-login failed')

    # set the account-wide shared secret
    pks.set_account(a, c, '_ss', domain_secret)
    if (rc != 'ok'):
        error('set_account(...%s...) failed: %s' % (account, rc))


    # Make sure a kite exists for each of the domains we're configuring
    for dom in ('blimp.{}'.format(domain)):
        rc, data = pks.add_kite(a, c, dom, False)
        if (rc != 'ok'): error('add_kite(%s) failed: %s' % (dom, rc))
        # set the per-kite shared secret
        rc, data = pks.set_account(a, c, '_ss:{}'.format(dom), domain_secret)
        if (rc != 'ok'): error('set_account(%s) failed: %s' % (dom, rc))


    # We don't set any DNS rules when we're not using Pagekite for DNS

    # # Configure a CNAME record ?
    # rc, data = pks.set_dns_records(a, c, domain, 'CNAME', 'pagekite.net')
    # if (rc != 'ok'):
    #     error('set_dns_record(%s, CNAME, ...) failed: %s' % (domain, rc))

    # Configure an MX record
    # rc, data = pks.set_dns_records(a, c, domain, 'MX', MX)
    # if (rc != 'ok'):
    #     error('set_dns_record(%s, MX, ...) failed: %s' % (domain, rc))
