import csv
from .models import Schema, Dataset
from django.core.files import File
import os
from .utils import make_generetions, generate_cache_task_key
from typing import Dict, List, Any


class FakeDataWrite:

    def _write_data_and_save_to_file(self, count: str, schema: Dict, file_name: str):
        column_separator = schema.column_separator
        string_character = schema.string_character
        to_csv = make_generetions(data=schema.fields, count=count)
        keys = to_csv[0].keys()
        with open(f"{file_name}.csv", "w+") as dataset_file:
            writer = csv.DictWriter(
                dataset_file,
                keys,
                delimiter=column_separator,
                quotechar=string_character,
            )
            writer.writeheader()
            writer.writerows(to_csv)

    def _save_file_to_db_and_remove_from_disc(self, file_name: str, user_id: str):
        with open(f"{file_name}.csv", "r") as dataset_file:
            Dataset.objects.create(file=File(dataset_file), user_id=user_id)
        os.remove(f"{file_name}.csv")

    def write_data_to_db_and_remove_from_disk(self, schema_id: str, count: str, user_id: str):
        schema = Schema.objects.get(id=schema_id)
        self._write_data_and_save_to_file(file_name=schema.name, schema=schema, count=count)
        self._save_file_to_db_and_remove_from_disc(file_name=schema.name, user_id=user_id)


class SchemaCreate:
    def __init__(self, data, user):
        self.data = data
        self.user = user

    def create_schema(self):
        name = self.data.get("name")
        column_separator = self.data.get("column_separator")
        string_character = self.data.get("string_character")
        fields = self.data.get("fields")

        schema = Schema.objects.create(
            name=name,
            column_separator=column_separator,
            string_character=string_character,
            fields=fields,
            user=self.user,
        )
        schema.save()


def start_download_dataset_task(schema_id: str, count: str, user_id: str) -> str:
    from .tasks import download_dataset_task
    cache_task_key = generate_cache_task_key()
    download_dataset_task(
        cache_task_key, schema_id=schema_id, count=count, user_id=user_id
    )
    return cache_task_key
