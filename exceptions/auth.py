from exceptions.base import BaseAppException


class InvalidUsernamePassword(BaseAppException):
    status_code = 401