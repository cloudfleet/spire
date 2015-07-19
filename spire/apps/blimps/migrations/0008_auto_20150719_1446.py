# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0007_auto_20150719_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blimp',
            name='owner',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
