from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.job import views


urlpatterns = patterns('',
    url(r'release', csrf_exempt(views.JobReleaseView.as_view()), name='release'),
)
