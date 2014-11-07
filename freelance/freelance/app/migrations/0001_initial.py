# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=100)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('history', models.CharField(max_length=150)),
                ('subtotal', models.FloatField(null=True, blank=True)),
                ('tax', models.FloatField(null=True, blank=True)),
                ('total', models.FloatField(null=True, blank=True)),
                ('file', models.FileField(upload_to=b'invoices/')),
                ('client', models.ForeignKey(to='app.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=b'todo/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
