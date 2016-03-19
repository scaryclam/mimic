from django.contrib import admin  # pragma: no cover

from apps.user import models  # pragma: no cover


admin.site.register(models.User)  # pragma: no cover

