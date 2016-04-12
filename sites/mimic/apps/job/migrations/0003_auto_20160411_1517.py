# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='last_released',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='max_assign_freq',
            field=models.PositiveIntegerField(default=0, help_text=b'Time, in seconds, that this job will NOT be reassigned for after release', null=True, blank=True),
        ),
    ]
