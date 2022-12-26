from typing import NoReturn

from fastapi import HTTPException, status


def _raise_http_exception(status_code: int, detail: str | None = None) -> NoReturn:
    raise HTTPException(status_code=status_code, detail=detail)


def raise_400_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_400_BAD_REQUEST, detail)


def raise_401_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_401_UNAUTHORIZED, detail)


def raise_402_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_402_PAYMENT_REQUIRED, detail)


def raise_403_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_403_FORBIDDEN, detail)


def raise_404_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_404_NOT_FOUND, detail)


def raise_408_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_408_REQUEST_TIMEOUT, detail)


def raise_409_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_409_CONFLICT, detail)


def raise_410_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_410_GONE, detail)


def raise_422_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, detail)


def raise_429_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_429_TOO_MANY_REQUESTS, detail)


def raise_503_exception(detail: str | None = None) -> NoReturn:
    _raise_http_exception(status.HTTP_503_SERVICE_UNAVAILABLE, detail)
