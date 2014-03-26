import logging

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import requests

from spire import settings

import docker
c = docker.Client(base_url='http://localhost:4444',
                  version='1.6',
                  timeout=10)

from plumbum import SshMachine
import os
from contextlib import contextmanager

@contextmanager
def blimpyard_tunnel():
    try:
        keyfile = os.path.expanduser(settings.BLIMPYARD_KEY)
    except AttributeError:
        keyfile = None
    url = settings.BLIMPYARD_URL
    user = settings.BLIMPYARD_USER
    docker_port = settings.DOCKER_PORT
    local_port = 4444

    with SshMachine(url, user=user, keyfile=keyfile) as blimpyard_host:
        with blimpyard_host.tunnel(local_port, docker_port):
            try:
                yield blimpyard_host
            finally:
                pass

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    subdomain = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    port = models.IntegerField(null=True, blank=True, default=None)

    def __unicode__(self):
        return str("{}'s {}".format(self.owner, self.subdomain))

    # TODO: put these two into some async job queue (celery?)

    # start blimp
    # sudo docker run -d -p 1338:1337 kermit/hellonode
    # sudo docker run -d -p 3001:3000 kermit/simple-ldap
    def start(self):
        """start the docker container"""
        with blimpyard_tunnel() as rem:
            # we get back the container id
            logging.info('* starting container')
            try:
                container = c.create_container(settings.DOCKER_IMAGE,
                                               name=self.subdomain,
                                               ports=[3000])
                c.start(container, publish_all_ports=True)
            except requests.exceptions.ConnectionError:
                container = None
            else:
                logging.info('* started container')
                info = c.inspect_container(container)
                self.port = info['NetworkSettings']['Ports']['3000'][0]['HostPort']
            self.save(update_fields=['port'])
            print('port is ' + str(self.port))
            # restart pagekite frontend
            # - call the Flask service that restarts pagekite
            logging.info('* calling pagekite restarter')
            rem['/usr/bin/wget localhost:5000 -o /dev/null']()
            return container

    def stop(self):
        """stop the container"""
        with blimpyard_tunnel():
            try:
                c.stop(self.subdomain)
                c.remove_container(self.subdomain)
            except requests.exception.ConnectionError:
                pass

    def url(self):
        # TODO: read from DB
        container_url = 'http://{}:{}'.format(settings.BLIMPYARD_URL, self.port)
        return container_url

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
