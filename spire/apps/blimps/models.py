import logging
import subprocess

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.mail import send_mail, mail_admins
from django.conf import settings
import requests

import docker
docker_base_url = 'http://{}:{}'.format(
    settings.SPIRE_DOCKER_API_HOST,
    settings.SPIRE_DOCKER_API_PORT
)
c = docker.Client(base_url=docker_base_url,
                  version='1.6',
                  timeout=10)

from plumbum import SshMachine
import os
from contextlib import contextmanager

#import redis

@contextmanager
def blimpyard_tunnel():
    try:
        keyfile = os.path.expanduser(settings.BLIMPYARD_KEY)
    except AttributeError:
        keyfile = None
    url = settings.BLIMPYARD_URL
    user = settings.BLIMPYARD_USER
    docker_port = settings.DOCKER_PORT
    local_port = settings.SPIRE_DOCKER_API_PORT

    with SshMachine(url, user=user, keyfile=keyfile) as blimpyard_host:
        with blimpyard_host.tunnel(local_port, docker_port):
            try:
                yield blimpyard_host
            finally:
                pass

def get_pagekite_frontend():
    if settings.BLIMPYARD_URL == 'localhost':
        cmd = "./scripts/docker_host_ip.sh"
        url = subprocess.check_output(cmd).decode().rstrip()
    else:
        url = settings.BLIMPYARD_URL
    port = settings.BLIMPYARD_PAGEKITE_PORT
    if port != 80:
        url = url + ':' + str(port)
    return url

# push notification to the frontend - work in progress
# r = redis.StrictRedis(host='localhost', port=6379, db=0)
# def push_notification():
#     """push notofication to frontend using Redis + Node.js"""
#     # TODO: add blimp id data to message
#     # TODO: test with Celery in another process
#     r.publish('spire-pusher', 'blimp ready')

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    subdomain = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    port = models.IntegerField(null=True, blank=True, default=None)
    ready = models.BooleanField(default=False)

    def __unicode__(self):
        return str("{}'s {}".format(self.owner, self.subdomain))

    def generate_backendsrc(self, path):
        with open(path, 'w') as f:
            for blimp in Blimp.objects.all():
                # TODO: use randomly generated password
                f.write(
                    'domain=http:{}:password\n'
                    .format(blimp.host())
                )

    # start blimp
    # sudo docker run -d -p 3001:3000 cloudfleet/cockpit
    def start(self):
        """start the docker container"""
        with blimpyard_tunnel() as rem:
            # start container
            logging.info('1. start container')
            try:
                pagekite_frontend = get_pagekite_frontend()
                secret = 'password' # TODO: randomly generate
                # test.localhost password 172.17.42.1:60666
                # we get back the container id

                environment = {
                    "CLOUDFLEET_DOMAIN": self.host(),
                    "CLOUDFLEET_SECRET": secret,
                    "CLOUDFLEET_HOST": pagekite_frontend
                }
                logging.debug(' - environment: ' + str(environment))

                container = c.create_container(settings.DOCKER_IMAGE,
                                               name=self.subdomain,
                                               environment=environment)
                c.start(container)
            except requests.exceptions.ConnectionError:
                logging.error(" - didn't start: connection error")
                container = None
            else:
                logging.info(' - {} container started'.format(settings.DOCKER_IMAGE))
                info = c.inspect_container(container)
                self.port = info['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']
                self.save(update_fields=['port'])
                logging.info('- docker exposed url: ' + self.url_exposed())

            # update backends.rc
            logging.info('2. update backends.rc')
            backendsrc_path = 'backends.rc'
            self.generate_backendsrc(backendsrc_path)
            rem.upload(backendsrc_path, '/etc/pagekite.d/20_backends.rc')

            # restart pagekite frontend
            logging.info('3. restart pagekite')
            # - call the Flask service that restarts pagekite
            rem['/usr/bin/wget localhost:5000 -o /dev/null']()

            # notify frontend to update the view
            #push_notification()
            return container

    def stop(self):
        """stop the container"""
        with blimpyard_tunnel():
            try:
                logging.debug('1. stop container')
                c.stop(self.subdomain)
                logging.debug('2. remove container')
                c.remove_container(self.subdomain)
                logging.info('- blimp deleted')
            except requests.exception.ConnectionError:
                logging.error('Connection error')

    def url_exposed(self):
        """as exposed through Docker"""
        container_url = 'http://{}:{}'.format(settings.BLIMPYARD_URL, self.port)
        return container_url

    def host(self):
        """just host (no port)"""
        # TODO: read from DB
        container_host = '{}.{}'.format(
            self.subdomain, settings.BLIMPYARD_URL
        )
        return container_host

    def url(self):
        """full url for external access"""
        # TODO: read from DB
        container_url = 'http://{}.{}:{}'.format(
            self.subdomain, settings.BLIMPYARD_URL,
            settings.BLIMPYARD_PAGEKITE_PORT
        )
        return container_url

    def notify_admin(self):
        """Notify the admins that a blimp was requested and needs manual
        activation.

        """
        subject = "{} awaits a blimp".format(self.owner)
        message = "User {} requested a blimp at url: {} .\n".format(
            self.owner, self.url()
        ) + "Make sure it works and activate it in the admin panel."
        mail_admins(subject, message)

    def notify_user_blimp_ready(self):
        """Notify the user that a requested blimp is ready."""
        subject = "blimp {} ready".format(self.url())
        message = "Hi {}, the blimp you requested is ready at: {} .".format(
            self.owner.username, self.url()
        )
        admin_email = settings.ADMINS[0][1]
        send_mail(subject, message, admin_email,
                  [self.owner.email])

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
