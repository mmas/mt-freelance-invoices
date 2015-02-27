# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150225_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='daily_rate',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 26, 13, 10, 57, 345032, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subtotal',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
