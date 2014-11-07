# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('number',)},
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='history',
        ),
        migrations.AddField(
            model_name='invoice',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 7, 7, 29, 27, 460059, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='date_paid',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(default=b'draft', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 7, 7, 29, 36, 347405, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
