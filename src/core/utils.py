"""Набор утилит."""

import json

from pydantic import BaseModel


def schema_model_dump(data: BaseModel) -> dict:
    try:
        return data.model_dump()
    except Exception as exc:
        to_create = data.model_dump_json()
        return json.loads(to_create)
