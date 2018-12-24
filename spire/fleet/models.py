from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now
from model_utils import FieldTracker

import logging

# Create your models here.
class Blimp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=100, unique=True)
    pagekite_secret = models.CharField(max_length=128)
    passphrase_tracker = FieldTracker(fields=["pagekite_secret"])

    def check_pagekite_secret(pagekite_secret_plain):
        return check_password(pagekite_secret_plain, pagekite_secret_hash)

    def save(self, *args, **kwargs):
        if self.passphrase_tracker.has_changed("pagekite_secret"):
            self.passphrase = make_password(self.pagekite_secret)
        super(Blimp, self).save(*args, **kwargs)

    def active_services(self):
        return [service.service_key for service in self.service_set.all() if service.is_active()]

    def is_active_service(self, service_key):
        return service_key in self.active_services()

    def __str__(self):
        return 'Blimp - ' + self.domain

    class Meta:
        ordering = ('created',)


class Service(models.Model):
    blimp = models.ForeignKey(Blimp, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_info = models.CharField(max_length=100)
    expires = models.DateTimeField()
    service_key = models.CharField(max_length=100)

    def __str__(self):
        return 'Service - ' + self.blimp.domain + ' - ' + self.service_key

    def is_active(self):
        return self.expires > now()

class Invite(models.Model):
    code = models.CharField(max_length=16)
    receiver = models.OneToOneField(Blimp, on_delete=models.CASCADE, related_name="received_invite", blank=True, null=True)
    used_for = models.ForeignKey(Blimp, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return 'Invite - ' + self.code
