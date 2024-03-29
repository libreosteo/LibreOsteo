# This file is part of LibreOsteo.
#
# LibreOsteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibreOsteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile
from django.contrib.auth import get_user_model, logout
from django.contrib.sessions.models import Session
from django.urls import reverse
import logging
from django.utils.deprecation import MiddlewareMixin
from libreosteoweb.models import OfficeSettings, LoggedInUser
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_login_url():
    return reverse(settings.LOGIN_URL_NAME)


def get_logout_url():
    return reverse(settings.LOGOUT_URL_NAME)


def initialize_admin_url():
    return reverse(settings.INITIALIZE_ADMIN_URL_NAME)


def no_reroute_pattern():
    no_reroute = []
    if hasattr(settings, 'NO_REROUTE_PATTERN_URL'):
        no_reroute += [
            compile(expr) for expr in settings.NO_REROUTE_PATTERN_URL
        ]
    return no_reroute


def get_exempts():
    exempts = [compile(get_login_url().lstrip('/'))]
    if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
        exempts += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
    return exempts


def get_authenticator():
    if hasattr(settings, "LIBREOSTEO_AUTHENTICATOR"):
        authenticator = [auth for auth in settings.LIBREOSTEO_AUTHENTICATOR][0]
        authenticator = import_string(authenticator)
        return authenticator()
    else:
        return FakeDummyAuthenticator()


class FakeDummyAuthenticator():

    def authenticate(self, request):
        pass


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than reverse(LOGIN_URL_NAME). Exemptions to this requirement can optionally
    be specified in settings via a list of regular expressions in
    LOGIN_EXEMPT_URLS (which you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that\
 doesn't work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."

        match_install = compile(initialize_admin_url().lstrip('/'))

        path = request.path.lstrip('/')

        UserModel = get_user_model()
        if any(m.match(path) for m in no_reroute_pattern()):
            return

        if UserModel.objects.all().count() == 0:
            logger.info("No user found")
            if not match_install.match(request.path.lstrip('/')):
                logger.info("redirect to install page")
                return HttpResponseRedirect(initialize_admin_url())
            else:
                logger.info("no redirect required")
                return

        if get_authenticator():
            # Try to authenticate the request
            try:
                get_authenticator().authenticate(request)
            except Exception as ex:
                logger.error(
                    "Request on %s %s, but authentication failed on authenticator"
                    % (request.method, request.path))
                return HttpResponseRedirect(get_login_url())

        if not request.user.is_authenticated:
            logger.info("user not authenticated")
            path = request.path.lstrip('/')
            if get_logout_url().lstrip('/') == path:
                request.path = ''
            if 'web-view' in path:
                request.path = ''
            if not any(m.match(path) for m in get_exempts()):
                logger.info(
                    "query path %s, authentication required. redirect to authentication form %s "
                    % (path, get_login_url()))
                return HttpResponseRedirect(get_login_url() + "?next=" +
                                            request.path)
        logger.info("user [%s] authenticated for %s %s" %
                    (request.user, request.method, request.path))


class OfficeSettingsMiddleware(MiddlewareMixin):
    """
    Middleware that sets `officesettings` attribute to request object.
    If this attribute is not set, it redirects to a form to select the office.
    """

    def process_request(self, request):
        assert hasattr(request, 'session'), "The Office Settings middleware\
 requires session middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.sessions.middleware.SessionMiddleware'."

        if not request.user.is_authenticated:
            return

        if hasattr(request, 'officesettings'):
            return

        path = request.path.lstrip('/')

        multiple_office = OfficeSettings.objects.all().count()
        request.has_multiple_office = multiple_office > 1
        if request.has_multiple_office:
            # Search into the session the current officesettings set
            current_officesettings = OfficeSettings.objects.filter(
                id=request.session.get('officesettings')).first()
            if current_officesettings is None:
                if any(m.match(path) for m in self.no_reroute_pattern()):
                    return
                # Redirect to the Office Settings form if not already
                # redirected
                if request.path != reverse('officesettings-set'):
                    return HttpResponseRedirect(reverse('officesettings-set'))
        else:
            current_officesettings = OfficeSettings.objects.first()
        request.officesettings = current_officesettings

    def no_reroute_pattern(self):
        no_reroute = []
        if hasattr(settings, 'OFFICE_SETTINGS_NO_REROUTE_PATTERN_URL'):
            no_reroute += [
                compile(expr)
                for expr in settings.OFFICE_SETTINGS_NO_REROUTE_PATTERN_URL
            ]
        return no_reroute


class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            if not hasattr(request.user, 'logged_in_user'):
                logout(request)
                return HttpResponseRedirect(get_login_url())
            stored_session_key = request.user.logged_in_user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                try:
                    Session.objects.get(
                        session_key=stored_session_key).delete()
                except:
                    LoggedInUser.objects.filter(user_id=request.user).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        return response
