# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151011_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
