# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import freelance.app.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150305_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='email_smtp_port',
            field=models.IntegerField(default=587),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 7, 15, 44, 46, 232909, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(upload_to=freelance.app.models.get_filename, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='settings',
            name='email_smtp',
            field=models.CharField(default=b'smtp.gmail.com', max_length=100),
            preserve_default=True,
        ),
    ]
