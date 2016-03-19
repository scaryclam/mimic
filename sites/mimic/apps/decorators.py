from functools import wraps

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


def login_forbidden(view_func, redirect_url='/'):
    """ Decorator that forbids access to page for logged in users
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(
                request, _("Page is not accessible for logged in users"))
            return redirect(redirect_url)
    return _checklogin

