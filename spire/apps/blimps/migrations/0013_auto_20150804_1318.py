# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0012_auto_20150801_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blimp',
            name='password',
            field=models.CharField(max_length=2047, blank=True),
        ),
    ]
