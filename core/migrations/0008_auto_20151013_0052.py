# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151013_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='active_session_key',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
