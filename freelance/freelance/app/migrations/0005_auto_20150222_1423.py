# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import freelance.app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150221_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.CharField(max_length=100, blank=True)),
                ('email_password', models.CharField(max_length=100, blank=True)),
                ('email_smtp', models.CharField(max_length=100, blank=True)),
                ('company_address', models.TextField()),
                ('company_info', models.TextField()),
                ('company_payment', models.TextField()),
                ('default_daily_rate', models.FloatField()),
                ('default_tax', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_info',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_payment',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_daily_rate',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_tax',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_smtp',
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.OneToOneField(null=True, to='app.Settings'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(upload_to=freelance.app.models.get_filename),
            preserve_default=True,
        ),
    ]
