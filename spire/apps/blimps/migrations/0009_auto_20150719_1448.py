# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0008_auto_20150719_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blimp',
            name='domain',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
