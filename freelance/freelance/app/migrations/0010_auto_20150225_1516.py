# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150225_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_from',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 15, 16, 33, 894398, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
