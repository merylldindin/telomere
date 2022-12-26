import json
from typing import Any

from bson import json_util


def dump_mongodb_results(data: Any) -> Any:
    return json.loads(json_util.dumps(data))


def load_mongodb_results(data: Any) -> Any:
    return json_util.loads(json.dumps(data))
