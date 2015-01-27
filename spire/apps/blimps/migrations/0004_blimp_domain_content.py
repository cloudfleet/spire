# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def domain_from_subdomain(apps, schema_editor):
    Blimp = apps.get_model("blimps", "Blimp")
    for blimp in Blimp.objects.all():
        blimp.domain = '{}.{}'.format(blimp.subdomain, settings.BLIMP_DOMAIN)
        blimp.save()

def clean_domain(apps, schema_editor):
    Blimp = apps.get_model("blimps", "Blimp")
    for blimp in Blimp.objects.all():
        blimp.domain = ''
        blimp.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0003_blimp_domain'),
    ]

    operations = [
        migrations.RunPython(domain_from_subdomain, clean_domain),
    ]
