# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150305_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='date_format',
            field=models.CharField(default=b'%d/%m/%Y', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 5, 23, 27, 49, 332424, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
