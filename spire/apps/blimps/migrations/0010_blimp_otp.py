# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0009_auto_20150719_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='OTP',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
