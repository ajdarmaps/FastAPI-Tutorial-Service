class InvalidUsernamePassword(Exception):
    status_code = 404
    pass


class PermissionDeniedError(Exception):
    status_code = 403
    pass