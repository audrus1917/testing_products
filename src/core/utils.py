"""Набор утилит."""

import json

from pydantic import BaseModel


def schema_model_dump(data: BaseModel) -> dict:
    try:
        return data.model_dump()
    except Exception as exc:
        to_create = data.model_dump_json()
        return json.loads(to_create)


def update_model_from_dict(model_instance, data_dict):
    for key, value in data_dict.items():
        if hasattr(model_instance, key):
            setattr(model_instance, key, value)