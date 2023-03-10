from typing import Dict, Any
from rest_framework import serializers
from .choices import (
    SCHEMA_COLUMN_SEPARATOR,
    SCHEMA_STRING_CHARACTER,
    SCHEMA_COLUMN_TYPE,
)
from .models import Schema, Dataset


class SchemaColumnSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=SCHEMA_COLUMN_TYPE)
    value_from = serializers.IntegerField(min_value=0, required=False)
    value_to = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = Schema
        fields = ["name", "type", "value_from", "value_to"]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data["type"] == "integer":
            return data

        value_from = data.get("value_from")
        value_to = data.get("value_to")

        if None in (value_from, value_to):
            raise serializers.ValidationError(
                "Values 'from_' and 'to' required with field with type 'integer'."
            )

        if value_from > value_to:
            raise serializers.ValidationError(
                "Value of field 'to' should be higher than value of field 'from_'."
            )

        return data


class CreateSchemaSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    column_separator = serializers.ChoiceField(choices=SCHEMA_COLUMN_SEPARATOR)
    string_character = serializers.ChoiceField(choices=SCHEMA_STRING_CHARACTER)
    fields = serializers.ListField(child=SchemaColumnSerializer(), allow_empty=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Schema
        fields = [
            "id",
            "name",
            "column_separator",
            "string_character",
            "fields",
            "user",
        ]


class DatasetSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(read_only=True)

    class Meta:
        model = Dataset
        fields = "__all__"
