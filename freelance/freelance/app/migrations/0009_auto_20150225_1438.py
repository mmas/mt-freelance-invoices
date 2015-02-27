# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150224_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='date_sent',
        ),
        migrations.AddField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 14, 38, 20, 203141, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
