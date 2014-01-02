from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import docker
c = docker.Client(base_url='http://localhost:4444',
                  version='1.6',
                  timeout=10)

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
        return c.images()

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
