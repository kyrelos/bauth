# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_mytoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='secondary_auth',
            field=models.BooleanField(default=False),
        ),
    ]
