# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150226_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='status',
        ),
        migrations.AddField(
            model_name='day',
            name='half',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 27, 14, 34, 20, 253666, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
