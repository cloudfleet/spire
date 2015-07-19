# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0006_auto_20150719_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blimp',
            name='subdomain',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
