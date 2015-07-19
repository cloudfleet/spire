# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blimps', '0005_auto_20150714_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='blimp',
            name='password',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='blimp',
            name='username',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='blimp',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
