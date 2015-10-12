# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('first_name', models.CharField(max_length=40, blank=True)),
                ('last_name', models.CharField(max_length=40, blank=True)),
                ('phone', models.CharField(unique=True, max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('occupation', models.CharField(max_length=100, null=True, blank=True)),
                ('monthly_income', models.CharField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, unique=True, null=True, blank=True)),
                ('county', models.CharField(max_length=100, null=True, blank=True)),
                ('nearest_town', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Lead',
                'verbose_name_plural': 'Leads',
            },
        ),
    ]
