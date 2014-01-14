from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import docker
c = docker.Client(base_url='http://localhost:4444',
                  version='1.6',
                  timeout=10)

from plumbum import SshMachine
import os
from contextlib import contextmanager

@contextmanager
def blimpyard_tunnel():
    _keyfile = os.path.expanduser('~/.ssh/blimpyard_rsa')
    _url = 'blimpyard.cloudfleet.io'

    with SshMachine(_url, user='kermit', keyfile=_keyfile) as _blimpyard_host:
        with _blimpyard_host.tunnel(4444,4243):
            try:
                yield
            finally:
                pass

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    subdomain = models.CharField(max_length=100)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return str("{}'s {}".format(self.owner, self.subdomain))

    # TODO: put these two into some async job queue (celery?)

    # start blimp
    # sudo docker run -d -p 1338:1337 kermit/hellonode
    def start(self):
        """start the docker container"""
        with blimpyard_tunnel():
            # we get back the container id
            container = c.create_container('kermit/hellonode',
                                            name=self.subdomain,
                                            ports=[1337])
            c.start(container, publish_all_ports=True)
            info = c.inspect_container(container)
            self.port = info['NetworkSettings']['Ports']['1337'][0]['HostPort']
            #self.save()
            print('port is ' + str(self.port))
            return container

    def stop(self):
        """stop the container"""
        with blimpyard_tunnel():
            c.stop(self.subdomain)
            c.remove_container(self.subdomain)

    def url(self):
        # TODO: read from DB
        container_url = 'blimpyard.cloudfleet.io:1338'
        return container_url

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
