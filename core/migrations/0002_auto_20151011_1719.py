# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_email_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_phone_validated',
            field=models.BooleanField(default=False),
        ),
    ]
