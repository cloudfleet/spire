# Generated by Django 2.0 on 2018-12-24 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_auto_20181223_0322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blimp',
            old_name='pagekite_secret_hash',
            new_name='pagekite_secret',
        ),
    ]
