# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='option key', choices=[(b'CACHE_INTERVAL', b'CACHE_INTERVAL'), (b'NOTIFICATIONS_ENABLED', b'NOTIFICATIONS_ENABLED')])),
                ('value', models.CharField(max_length=255, verbose_name='option value', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, help_text='when off \u2013 default value will be used', verbose_name='is active')),
            ],
            options={
                'verbose_name': 'database option',
                'verbose_name_plural': 'database options',
            },
        ),
    ]
