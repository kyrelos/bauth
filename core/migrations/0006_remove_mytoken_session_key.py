# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mytoken_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mytoken',
            name='session_key',
        ),
    ]
