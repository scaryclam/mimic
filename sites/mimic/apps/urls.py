from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from apps import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="home"),
    url(r'agent/', include('apps.agent.urls', namespace="agent")),
    url(r'job/', include('apps.job.urls', namespace="job")),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    from django.views.generic import TemplateView

    urlpatterns += staticfiles_urlpatterns()

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    #urlpatterns += [
    #    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    #]


urlpatterns += [
    url(r'', include('apps.consumer.urls')),
]

