import itertools
import re
from collections.abc import Iterable
from typing import Any

PLACEHOLDER = "%s"
MYSQL_CONNECT_TIMEOUT = 10
MAX_PLACEHOLDERS_COUNT = 65535

MULTI_SPACE_REGEX = r"\s+"
compiled_multi_space_regex = re.compile(MULTI_SPACE_REGEX)


def _is_iterable(value: Any) -> bool:
    return isinstance(value, Iterable) and not isinstance(value, str)


def _escape_column_name(column: str) -> str:
    return f"`{column}`"


def _flatten_values(values: tuple) -> tuple:
    return tuple(
        itertools.chain.from_iterable(
            list(value) if _is_iterable(value) else (value,) for value in values
        )
    )


def _get_placeholder_indexes(statement: str) -> list[int]:
    return [occurence.start(0) for occurence in re.finditer(r"\?", statement)]


def _expand_placeholder_lists(
    placeholder_indexes: list[int], statement: str, values: tuple | None
) -> str:
    offset = 0
    for placeholder_index, value in zip(placeholder_indexes, values):
        if _is_iterable(value):
            placeholder = f"({', '.join([PLACEHOLDER for _ in value])})"
            statement = (
                statement[: placeholder_index + offset]
                + placeholder
                + statement[placeholder_index + offset + 1 :]
            )
            offset = offset + len(placeholder) - 1

    return statement


def _compile_statement(statement: str) -> str:
    return compiled_multi_space_regex.sub(" ", statement).replace("?", PLACEHOLDER)


def _format_statement(
    statement: str, values: tuple | None = None, limit: int | None = None
) -> str:
    placeholder_indexes = _get_placeholder_indexes(statement)
    limited_statement = "" if limit is None else f" LIMIT {limit}"

    if (count_placeholders := len(placeholder_indexes)) == 0:
        return _compile_statement(statement) + limited_statement

    if values is None or count_placeholders != len(values):
        raise ValueError("Placeholders and values do not match")

    expanded_statement = _expand_placeholder_lists(
        placeholder_indexes, statement, values
    )

    return _compile_statement(expanded_statement) + limited_statement


def format_query(
    statement: str, values: tuple | None = None, limit: int | None = None
) -> tuple[str, tuple]:
    if values is None:
        values = ()

    formatted_statement = _format_statement(statement, values=values, limit=limit)
    flattened_values = _flatten_values(values)

    return (formatted_statement, flattened_values)


def get_max_batch_size_from_item(item: dict) -> int:
    count_attributes = len(item.keys())

    return int(MAX_PLACEHOLDERS_COUNT / count_attributes)


def build_insertion_query(
    table_name: str, items: list[dict], strict: bool = True
) -> tuple[str, tuple]:
    strictness = "" if strict else "IGNORE "

    sorted_keys = sorted(list(items[0].keys()))
    table_column_names = ",".join(
        [_escape_column_name(attribute) for attribute in sorted_keys]
    )

    item_placeholders = ",".join([PLACEHOLDER for _ in sorted_keys])
    placeholders = ", ".join([f"({item_placeholders})" for _ in items])

    sorted_values = tuple(
        itertools.chain.from_iterable(
            [[item.get(key) for key in sorted_keys] for item in items]
        )
    )

    return (
        (
            f"INSERT {strictness}"
            f"INTO {table_name} ({table_column_names}) "
            f"VALUES {placeholders}"
        ),
        sorted_values,
    )
