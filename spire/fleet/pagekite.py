import sys
from xmlrpc.client import ServerProxy
import logging

ADMIN_ACCOUNT = 'cloudfleet.pagekite.me'
ADMIN_EMAIL = 'christoph+%s@doublemalt.net'

# SOA = "bre.pagekite.me. 2015080100 3600 3600 7200 300"
# EMAIL = 'bre+%s@pagekite.net'
# ACCOUNT = 'klakibre.pagekite.me'
# DOMAIN = 'cloudfleet-fake-test.com'
# SECRET = getpass.getpass('Password for %s: ' % ADMIN)

def error(msg):
    logging.error('{}'.format(msg))

def _get_server():
    return ServerProxy('https://pagekite.net/xmlrpc/')

def create_pagekite_account(domain, domain_secret, admin_secret):
    pagekite = _get_server()

    account_name = domain.replace('.', '-') + '.myblimp.net'


    _, (admin_account_id, admin_cred) = pagekite.login(ADMIN_ACCOUNT, admin_secret, '')

    pagekite.create_account(admin_account_id, admin_cred,
                                  ADMIN_EMAIL % account_name, account_name,
                                  True, False, True)  # terms, mail, activate

    _, (account_id, __) = pagekite.login(account_name, (admin_account_id, admin_cred), '')

    pagekite.set_account(account_id, (admin_account_id, admin_cred), '_ss', domain_secret)



def update_blimp_kites(domain, domain_secret, admin_secret, subdomains):
    pagekite = _get_server()

    _, (admin_account_id, admin_cred) = pagekite.login(ADMIN_ACCOUNT, admin_secret, '')
    _, (account_id, __) = pagekite.login(account_name, (admin_account_id, admin_cred), '')

    #FIXME check existing kites pagekite.get_account_info(account_id, (admin_account_id, admin_cred))

    for subdomain in subdomains:
        fqdn = subdomain + "." + domain
        pagekite.add_kite(account_id, (admin_account_id, admin_cred), fqdn, False)
        pagekite.set_dns_records(account_id, (admin_account_id, admin_cred), fqdn, 'CNAME', 'pagekite.me')
