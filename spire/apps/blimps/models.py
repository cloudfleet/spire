from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """
    # TODO: random number as serial
    subdomain = models.CharField(max_length=100)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return str("{}'s {}".format(self.owner, self.subdomain))

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['subdomain']
