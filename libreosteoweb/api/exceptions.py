from rest_framework.exceptions import APIException

class Forbidden(APIException):
    status_code = 403
    default_detail = 'This operation is forbidden.'