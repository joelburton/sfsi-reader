"""
Additional middleware for our site.
"""

from django.http import HttpResponseRedirect
from django.conf import settings


EXEMPT_URLS = [settings.LOGIN_URL] + getattr(settings, 'LOGIN_EXEMPT_URLS', [])
EXEMPT_URLS = [url.lstrip('/') for url in EXEMPT_URLS]


class LoginRequiredMiddleware(object):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    @staticmethod
    def process_request(request):
        if request.user.is_anonymous():
            path = request.path_info.lstrip('/')
            if not any(path.startswith(exempt) for exempt in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)