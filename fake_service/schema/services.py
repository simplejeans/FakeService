import csv
from schema.models import Schema, Dataset
from django.core.files import File
import os
from schema.utils import generate_fake_data, generate_cache_task_key
from typing import Dict, List, Any


class FakeDataWrite:

    def _write_data_and_save_to_file(self, row_nums: str, schema: Dict, file_name: str):
        column_separator = schema.column_separator
        string_character = schema.string_character
        data_to_csv = generate_fake_data(data=schema.fields, row_nums=row_nums)
        column_names = data_to_csv[0].keys()
        with open(f"{file_name}.csv", "w+") as dataset_file:
            writer = csv.DictWriter(
                dataset_file,
                column_names,
                delimiter=column_separator,
                quotechar=string_character,
            )
            writer.writeheader()
            writer.writerows(data_to_csv)

    def _save_file_to_db_and_remove_from_disc(self, file_name: str, user_id: str):
        with open(f"{file_name}.csv", "r") as dataset_file:
            Dataset.objects.create(file=File(dataset_file), user_id=user_id)
        os.remove(f"{file_name}.csv")

    def write_data_to_db_and_remove_from_disk(self, schema_id: str, row_nums: str, user_id: str):
        schema = Schema.objects.get(id=schema_id)
        self._write_data_and_save_to_file(file_name=schema.name, schema=schema, row_nums=row_nums)
        self._save_file_to_db_and_remove_from_disc(file_name=schema.name, user_id=user_id)

