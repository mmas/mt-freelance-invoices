# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150307_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'ordering': ('code',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='settings',
            name='email_password',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 8, 16, 55, 21, 849206, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
