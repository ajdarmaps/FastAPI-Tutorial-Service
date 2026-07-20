class UserNotFoundError(Exception):
    status_code = 404
    pass


class UserAlreadyExistsError(Exception):
    status_code = 404
    pass

