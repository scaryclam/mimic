# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('producer_type', models.CharField(max_length=100)),
                ('output_template', models.TextField()),
                ('frequency', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
