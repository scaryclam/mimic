from django.conf.urls import patterns, include, url

from apps.consumer.views import ConsumerView


urlpatterns = patterns('',
    url(r'^((?:[\w\-]+/)*)$', ConsumerView.as_view()),
)

