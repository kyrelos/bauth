# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151013_0052'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Lead',
        ),
        migrations.AlterModelOptions(
            name='mytoken',
            options={'verbose_name': 'Auth Token', 'verbose_name_plural': 'Auth Tokens'},
        ),
    ]
