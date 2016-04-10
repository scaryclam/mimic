# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agent_id', models.CharField(max_length=200)),
                ('registered_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_checkin_datetime', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
