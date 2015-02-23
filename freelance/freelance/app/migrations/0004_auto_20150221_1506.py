# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import freelance.app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20141107_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=100)),
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
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('invoice', models.ForeignKey(related_name='days_worked', to='app.Invoice', null=True)),
            ],
            options={
                'ordering': ('date',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-created',)},
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='date',
            new_name='date_sent',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='file',
            new_name='pdf',
        ),
        migrations.AddField(
            model_name='invoice',
            name='daily_rate',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(default='', max_length=75),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(to='app.Client', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
