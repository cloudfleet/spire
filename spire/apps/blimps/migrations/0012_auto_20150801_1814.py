# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models, migrations
import scrypt

def hash_passwords(apps, schema_editor):
    Blimp = apps.get_model("blimps", "Blimp")
    for blimp in Blimp.objects.all():
        blimp.password = scrypt.encrypt(
            os.urandom(64), blimp.password, maxtime=0.5
        ).decode('latin1')
        blimp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0011_blimp_secret'),
    ]

    operations = [
        migrations.RunPython(hash_passwords),
    ]
