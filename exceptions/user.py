from exceptions.base import BaseAppException


class UserNotFoundError(BaseAppException):
    status_code = 404


class UserAlreadyExistsError(BaseAppException):
    status_code = 409