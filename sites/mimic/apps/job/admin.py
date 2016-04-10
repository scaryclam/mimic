from django.contrib import admin  # pragma: no cover

from apps.job import models  # pragma: no cover


admin.site.register(models.Job)  # pragma: no cover
admin.site.register(models.JobType)  # pragma: no cover
admin.site.register(models.JobMeta)  # pragma: no cover
