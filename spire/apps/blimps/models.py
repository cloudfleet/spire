from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import docker
c = docker.Client(base_url='http://localhost:4444',
                  version='1.6',
                  timeout=10)
import bgtunnel
import os
import requests

def start_tunnel():
    # TODO: put exact details in settings.py
    forwarder = bgtunnel.open(ssh_user='kermit',
                                  ssh_address='blimpyard.cloudfleet.io',
                                  host_port='4243', bind_port='4444',
                                  identity_file=os.path.expanduser('~/.ssh/blimpyard_rsa'))

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    subdomain = models.CharField(max_length=100)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return str("{}'s {}".format(self.owner, self.subdomain))

    # start blimp
    # sudo docker run -d -p 1338:1337 kermit/hellonode
    def start(self):
        # TODO: use with
        try:
            return c.images()
        except requests.ConnectionError:
            start_tunnel()
            return c.images()

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
