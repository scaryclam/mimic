from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.agent import views


urlpatterns = patterns('',
    url(r'register', csrf_exempt(views.AgentRegisterView.as_view()), name='register'),
    url(r'jobs/request', views.AgentJobsRequestView.as_view(), name='request_jobs'),
)
