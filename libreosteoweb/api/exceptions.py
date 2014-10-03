from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _

class AlreadyExistsException(APIException):
    status_code = 403
    default_detail = _('This patient already exists')
