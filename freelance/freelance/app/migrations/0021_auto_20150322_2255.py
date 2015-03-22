# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20150308_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='email_protocol',
            field=models.IntegerField(default=0, choices=[(0, b'tsl'), (1, b'ssl')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 22, 22, 55, 17, 942472, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
