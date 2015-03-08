# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20150308_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=70),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 8, 17, 2, 9, 652994, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
