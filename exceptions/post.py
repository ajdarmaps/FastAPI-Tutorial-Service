from exceptions.base import BaseAppException


class PostNotFoundError(BaseAppException):
    status_code = 404