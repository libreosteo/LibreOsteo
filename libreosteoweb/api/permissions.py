
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .exceptions import Forbidden
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsStaffOrReadOnlyTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        try :
            return getattr(obj, 'user') == request.user
        except AttributeError:
            return obj == request.user


class IsStaffOrTargetUserFactory(object):
    @staticmethod
    def additional_methods(methods_list):
        return type('IsStaffOrTargetUser', (IsStaffOrTargetUser,), {'extra_actions': methods_list})

class IsStaffOrTargetUser(permissions.BasePermission):
    all_user_actions = [
        'create',
        'retrieve',
        'partial_update',
        'update'
    ]

    extra_actions = []

    def permitted_actions(self):
        return self.all_user_actions + self.extra_actions

    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return (view.action in self.permitted_actions()) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        if request.user.is_staff:
        	return True

        try :
        	return getattr(obj, 'user') == request.user
        except AttributeError:
        	return obj == request.user

from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.db import OperationalError

def maintenance_available():
    """
    A decorator for indicating if a function is available or not, otherwise raise an 
    HttpException(400)

    @maintenance_available
    def display_restore_database(request):
        ...
    """

    def _decorator(func):
        UserModel = get_user_model()
        try:
            if UserModel.objects.all().count() == 0 :
                if(func) :
                    return func
            else :
                return HttpResponseForbidden
        except :
            return HttpResponseForbidden
    return _decorator

class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('login'))
        return super(StaffRequiredMixin, self).dispatch(request,*args, **kwargs)
