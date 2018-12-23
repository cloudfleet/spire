# Generated by Django 2.0 on 2018-01-29 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0003_auto_20180129_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='receiver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_invite', to='fleet.Blimp'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='used_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.Blimp'),
        ),
    ]
