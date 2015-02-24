# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150222_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='default_daily_rate',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_tax',
            field=models.FloatField(default=0.2),
            preserve_default=True,
        ),
    ]
