# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150227_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='saved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 27, 14, 41, 55, 487735, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
