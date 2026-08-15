from exceptions.base import BaseAppException


class PermissionDeniedError(BaseAppException):
    status_code = 403