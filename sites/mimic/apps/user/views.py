from django.views.generic import FormView, RedirectView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from apps.user import forms
from apps.user.services import UserService


class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = forms.LoginForm
    redirect_field_name = 'next'

    def get_form_kwargs(self):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return HttpResponseRedirect(form.cleaned_data['redirect_url'])

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        super(LogoutView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('user:login'))

