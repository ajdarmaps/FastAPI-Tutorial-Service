class BaseAppException(Exception):
    status_code: int = 500

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)