# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='signature',
            field=models.FileField(default=None, null=True, blank=True, upload_to='blimps'),
            preserve_default=True,
        ),
    ]
