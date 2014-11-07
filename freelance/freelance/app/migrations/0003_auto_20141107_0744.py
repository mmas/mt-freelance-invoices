# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20141107_0729'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
    ]
