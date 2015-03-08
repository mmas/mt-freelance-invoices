# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20150308_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='currency',
            field=models.ForeignKey(default=1000, to='app.Currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 8, 17, 16, 50, 783429, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
