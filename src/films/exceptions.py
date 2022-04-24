from typing import Optional


class BaseFilmException(Exception):
    """Базовый класс ошибок"""


class TimeoutException(BaseFilmException):
    """Ошибка времени ожидания"""

    def __init__(self, url: str, timeout: Optional[int]):
        self.url = url
        self.timeout = timeout

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.url=} {self.timeout=})"


class NotFoundException(BaseFilmException):
    """Not found"""

    def __init__(self, url: str):
        self.url = url

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.url=})"


class UnexpectedException(BaseFilmException):
    """Unexpected"""

    def __init__(self, error: str, status_code: int):
        self.error = error
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.error=} {self.status_code=})"
