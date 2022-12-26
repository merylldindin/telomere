from typing import Any

import pymysql

from src.utils.exceptions import raise_400_exception
from src.utils.settings import IS_DEVELOPMENT

MYSQL_EXCEPTIONS = (
    pymysql.err.IntegrityError,
    pymysql.err.OperationalError,
    pymysql.err.ProgrammingError,
)


def catch_mysql_exceptions():
    def inner_decorator(function):
        def wrapper(self, *args, **kwargs) -> Any:
            try:
                return function(self, *args, **kwargs)
            except MYSQL_EXCEPTIONS as error:
                if IS_DEVELOPMENT:
                    print(error)
                    return None

                raise_400_exception(str(error))

        return wrapper

    return inner_decorator
