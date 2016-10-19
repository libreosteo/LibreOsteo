from rest_framework import permissions
from django.contrib.auth import get_user_model
from .exceptions import Forbidden
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

class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return (view.action in ['create', 'retrieve', 'partial_update', 'update']) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        if request.user.is_staff:
        	return True

        try :
        	return getattr(obj, 'user') == request.user
        except AttributeError:
        	return obj == request.user

from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponseForbidden

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
        if UserModel.objects.all().count() == 0 :
            if(func) :
                return func
        else :
            return HttpResponseForbidden
    return _decorator
