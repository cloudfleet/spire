# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0004_blimp_domain_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='cert',
            field=models.TextField(default=None, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blimp',
            name='cert_req',
            field=models.TextField(default=None, blank=True, null=True),
        ),
    ]
