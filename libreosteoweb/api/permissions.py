from rest_framework import permissions
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return (view.action in ['retrieve', 'partial_update', 'update']) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        if request.user.is_staff:
        	return True
        try :
        	return getattr(obj, 'user') == request.user
        except AttributeError:
        	return obj == request.user
