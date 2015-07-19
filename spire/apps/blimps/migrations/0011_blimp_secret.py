# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0010_blimp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='secret',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
