# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_account_secondary_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytoken',
            name='session_key',
            field=models.CharField(default='2apbkbeikuw0ohm00e77inu03zr8gg3o', max_length=32),
            preserve_default=False,
        ),
    ]
