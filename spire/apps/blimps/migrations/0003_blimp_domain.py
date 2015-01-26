# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0002_blimp_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='domain',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]
