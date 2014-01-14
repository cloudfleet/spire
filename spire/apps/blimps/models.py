from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import docker
_docker = docker.Client(base_url='http://localhost:4444',
                  version='1.6',
                  timeout=10)
import plumbum
import os
_keyfile = os.path.expanduser('~/.ssh/blimpyard_rsa')
_blimpyard = plumbum.SshMachine('blimpyard.cloudfleet.io',
                                user='kermit',
                                keyfile=_keyfile)

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
        """start the docker container"""
        with _blimpyard.tunnel(4444,4243):
            # we get back the container id
            # TODO: something is still wrong with the container port config
            container = _docker.create_container('kermit/hellonode',
                                                 name=self.subdomain)
            blimp_port = 1338
            _docker.start(container, port_bindings={1337: ('0.0.0.0', blimp_port)})
            # TODO: store container info in DB
            return str(container)

    def stop(self):
        """stop the container"""
        with _blimpyard.tunnel(4444,4243):
            _docker.stop(self.subdomain)
            _docker.remove_container(self.subdomain)

    def url(self):
        # TODO: read from DB
        container_url = 'blimpyard.cloudfleet.io:1338'
        return container_url

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
