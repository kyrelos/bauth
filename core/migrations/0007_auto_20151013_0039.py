# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_mytoken_session_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mytoken',
            options={'verbose_name': 'Lead', 'verbose_name_plural': 'Leads'},
        ),
        migrations.AddField(
            model_name='account',
            name='active_session_key',
            field=models.CharField(default='2apbkbeikuw0ohm00e77inu03zr8gg3o', max_length=32),
            preserve_default=False,
        ),
    ]
