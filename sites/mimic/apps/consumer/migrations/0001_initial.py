# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('consumer_type', models.CharField(max_length=100)),
                ('expected_template', models.TextField(null=True, blank=True)),
                ('frequency_limit', models.IntegerField(null=True, blank=True)),
                ('endpoint', models.CharField(unique=True, max_length=512)),
            ],
        ),
    ]
