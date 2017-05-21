import logging
import subprocess

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins
from django.core.urlresolvers import reverse
from django.conf import settings
import requests

import os
from contextlib import contextmanager

#import redis

from . import lib


class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    # TODO: remove subdomain when domain is fully functional
    subdomain = models.CharField(max_length=100, blank=True)
    domain = models.CharField(max_length=100, unique=True)
    # optional user on Spire who owns the blimp
    owner = models.ForeignKey(User, null=True, blank=True)
    # the username & pw for logging into the physical blimp the first time
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=2047, blank=True) # hashed password
    # one-time password used in the blimp-spire communication workflow
    OTP = models.CharField(max_length=255, blank=True)
    # a shared secret accessible to the blimp, spire, mail relay and pagekite
    secret = models.CharField(max_length=255, blank=True)
    port = models.IntegerField(null=True, blank=True, default=None)
    ready = models.BooleanField(default=False)
    # TODO: remove signature as a file - replace with certificate_request
    signature = models.FileField(upload_to='blimps',
                                 null=True, blank=True, default=None)
    cert_req = models.TextField(null=True, blank=True, default=None)
    cert = models.TextField(null=True, blank=True, default=None)

    def __unicode__(self):
        return str("{}@{}".format(self.username, self.domain))

    def __str__(self):
        return self.__unicode__()

    def generate_backendsrc(self, path):
        with open(path, 'w') as f:
            for blimp in Blimp.objects.all():
                # TODO: use randomly generated password
                f.write(
                    'domain=http:{}:password\n'
                    .format(blimp.host())
                )


    def url_exposed(self):
        """as exposed through Docker"""
        container_url = 'http://{}:{}'.format(settings.BLIMPYARD_URL, self.port)
        return container_url

    def host(self):
        """domain with subdomain included, e.g. blimp.jules.org"""
        host_str = '{}.{}'.format(
            settings.BLIMP_SUBDOMAIN, self.domain
        )
        return host_str

    def url(self):
        """full url for external access, e.g. http://blimp.jules.org"""
        return 'https://{}'.format(self.host())

    def get_admin_url(self):
        """the url to the Django admin interface for the model instance"""
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    def notify_admin(self):
        """Notify the admins that a blimp was ordered.

        """
        subject = "blimp {} ordered".format(self)
        message = """
        Blimp {} ordered.

        1) Copy the OTP from <a href="https://spire.cloudfleet.io{}">here</a>.
        2) Register domain, prepare and ship the device with the OTP.
        """.format(
            self,
            self.get_admin_url()
        )
        mail_admins(subject, message)

    def hash_password(self):
        """Hash self.password. Do this before storing instance to DB!"""
        self.password = lib.hash_password(self.password)

    def verify_password(self, password):
        """If cleartext @param password matches the hashed password in the DB"""
        return lib.verify_password(self.password, password)

    def generate_OTP(self):
        """Generate a one-time password (OTP). This is sent with the physical
        blimp. Doesn't save to DB - call blimp.save() separately.

        """
        self.OTP = lib.generate_password()

    def generate_secret(self):
        """Generate a shared secret that will be accessible to the blimp, spire,
        mail relay and pagekite.

        """
        self.secret = lib.generate_password(40)

    def notify_admin_signature(self, signature_url):
        """Notify admin that a signature is uploaded"""
        subject = "{} needs an SSL certificate.".format(self.host())
        message = "Signature for {} uploaded. Download: {} .".format(
            self.host(), signature_url
        )
        mail_admins(subject, message)

    def notify_admin_cert_req(self, edit_url):
        """Notify admin that a cert_req has arrived"""
        subject = "{} needs an SSL certificate.".format(self.host())
        message = "Signature for {} uploaded. Process:\n{}".format(
            self.host(), edit_url
        )
        mail_admins(subject, message)

    def notify_periscope_cert_ready(self):
        """API notification to the physical blimp that the signed certificate is
        ready

        """
        lib.notify_periscope_cert_ready(self)

    def notify_user_blimp_ready(self):
        """Notify the user that a requested blimp is ready."""
        subject = "blimp {} ready".format(self.url())
        message = "Hi {}, the blimp you requested is ready at: {} .".format(
            self.owner.username, self.url()
        )
        admin_email = settings.ADMINS[0][1]
        send_mail(subject, message, admin_email,
                  [self.owner.email])
