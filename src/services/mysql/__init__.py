import pymysql
import pymysql.cursors

from src.utils.decorators import catch_mysql_exceptions
from src.utils.exceptions import raise_400_exception

from .settings import MYSQL_SETTINGS, StrictMysqlSettings
from .utils import (
    MYSQL_CONNECT_TIMEOUT,
    build_insertion_query,
    format_query,
    get_max_batch_size_from_item,
)

DEFAULT_ERROR_MESSAGE = "No instance connected"


class MysqlSignature:
    def run_many(self, _: list[str], __: list[tuple | None] | None = None) -> int:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def run_one(self, _: str, __: tuple | None = None) -> int:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def read_many(
        self, _: str, __: tuple | None = None, ___: int | None = 1000
    ) -> list[dict]:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def read_one(self, _: str, __: tuple | None = None) -> dict | None:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def create_many(self, _: str, __: list[dict], ___: bool = True) -> int:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def create_one(self, _: str, __: dict, ___: bool = True) -> int:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def list_schemas(self) -> dict | None:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)

    def list_constraints(self) -> list:
        raise_400_exception(DEFAULT_ERROR_MESSAGE)


class MysqlService:
    def __init__(self) -> None:
        self._settings = StrictMysqlSettings(**MYSQL_SETTINGS.dict())

    def _connect(self) -> pymysql.connections.Connection:
        return pymysql.connect(
            host=self._settings.host,
            database=self._settings.database,
            user=self._settings.user,
            password=self._settings.password,
            port=self._settings.port,
            connect_timeout=MYSQL_CONNECT_TIMEOUT,
            cursorclass=pymysql.cursors.DictCursor,
        )

    @catch_mysql_exceptions()
    def run_many(
        self, statements: list[str], values: list[tuple | None] | None = None
    ) -> int:
        if values is None:
            values = [None for _ in range(len(statements))]

        affected_rows = 0

        with self._connect() as connection:
            with connection.cursor() as cursor:
                for statement, value in zip(statements, values):
                    formatted_statement, flattened_values = format_query(
                        statement, value
                    )

                    affected_rows += cursor.execute(
                        formatted_statement, flattened_values
                    )

            connection.commit()

        return affected_rows

    def run_one(self, statement: str, values: tuple | None = None) -> int:
        return self.run_many([statement], [values])

    @catch_mysql_exceptions()
    def read_many(
        self, statement: str, values: tuple | None = None, limit: int | None = 1000
    ) -> list[dict]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                formatted_statement, flattened_values = format_query(
                    statement, values, limit=limit
                )
                cursor.execute(formatted_statement, flattened_values)

                return results if len(results := cursor.fetchall()) > 0 else []

    def read_one(self, statement: str, values: tuple | None = None) -> dict | None:
        results = self.read_many(statement, values, limit=1)

        return None if len(results) == 0 else results[0]

    @catch_mysql_exceptions()
    def create_many(self, table: str, items: list[dict], strict: bool = True) -> int:
        if not items:
            return 0

        new_rows = 0
        batch_size = get_max_batch_size_from_item(items[0])

        with self._connect() as connection:
            with connection.cursor() as cursor:
                for batch_index in range(0, len(items), batch_size):
                    items_batch = items[batch_index : batch_index + batch_size]

                    if len(items_batch) > 0:
                        statement, values = build_insertion_query(
                            table, items_batch, strict=strict
                        )

                        formatted_statement, flattened_values = format_query(
                            statement, values
                        )

                        new_rows += cursor.execute(
                            formatted_statement, flattened_values
                        )

            connection.commit()

        return new_rows

    def create_one(self, table: str, item: dict, strict: bool = True) -> int:
        return self.create_many(table, [item], strict=strict)

    def list_schemas(self) -> dict | None:
        if (tables := self.read_many("SHOW TABLES", limit=None)) is None:
            return None

        description = f"Tables_in_{self._settings.database}"

        return {
            table.get(description): {
                attribute["Field"]: attribute["Type"].upper()
                + f"{' NOT NULL' if attribute.get('Null') == 'NO' else ''}"
                for attribute in self.read_many(
                    f"DESCRIBE {table.get(description)}", limit=None
                )
            }
            for table in tables
        }

    def list_constraints(self) -> list:
        return self.read_many(
            f"SELECT fks.table_name AS foreign_table, \
                fks.referenced_table_name AS primary_table, \
                fks.constraint_name AS name \
            FROM information_schema.referential_constraints fks \
            JOIN information_schema.key_column_usage kcu \
                ON fks.constraint_schema = kcu.table_schema \
                AND fks.table_name = kcu.table_name \
                AND fks.constraint_name = kcu.constraint_name \
            WHERE fks.constraint_schema = '{self._settings.database}' \
            GROUP BY fks.constraint_schema, \
                fks.table_name, \
                fks.unique_constraint_schema, \
                fks.referenced_table_name, \
                fks.constraint_name \
            ORDER BY fks.constraint_schema, \
                fks.table_name",
            limit=None,
        )
