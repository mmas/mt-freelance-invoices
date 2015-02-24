# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150224_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='company_payment',
        ),
        migrations.AddField(
            model_name='settings',
            name='company_account',
            field=models.CharField(default='', max_length=50, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='company_name',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings',
            name='company_address',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='settings',
            name='company_info',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
