from django.db import models

class Blimp(models.Model):
    """a magical box that flies over to someone and provides secure,
    web-based e-mail and file syncing

    """

    serial = models.IntegerField()

    def __unicode__(self):
        return str(self.serial)
