from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.user import views
from apps.decorators import login_forbidden


urlpatterns = patterns('',
    url(r'^login/$', login_forbidden(views.LoginView.as_view()), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
)

