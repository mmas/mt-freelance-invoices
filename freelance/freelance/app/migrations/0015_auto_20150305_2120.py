# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20150227_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='saved',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 5, 21, 20, 43, 385308, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updated',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
