from typing import Any, Dict

from rest_framework import request

from .models import Schema


def create_schema(data: Dict[str, Any], user) -> None:
    name = data.get("name")
    column_separator = data.get("column_separator")
    string_character = data.get("string_character")
    fields = data.get("fields")

    schema = Schema.objects.create(
        name=name, column_separator=column_separator, string_character=string_character, fields=fields,
        user=user
    )
    schema.save()
