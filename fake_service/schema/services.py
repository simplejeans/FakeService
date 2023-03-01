import csv
from faker import Faker
from faker.generator import random
from schema.models import Schema, Dataset
from django.core.files import File
import os
from typing import Dict, List, Any


class DatasetCreatorService:

    def _save_dataset_file_to_db_and_remove_from_disc(self, file_name: str, user_id: str):
        with open(f"{file_name}.csv", "r") as dataset_file:
            Dataset.objects.create(file=File(dataset_file), user_id=user_id)
        os.remove(f"{file_name}.csv")

    def create_dataset_file(self, schema_id: str, row_nums: int, user_id: str):
        schema = Schema.objects.get(id=schema_id)
        FakeDataCSVFileWriterService().create_csv_file_with_fake_data(file_name=schema.name, schema=schema, row_nums=row_nums)
        self._save_dataset_file_to_db_and_remove_from_disc(file_name=schema.name, user_id=user_id)


class FakeDataCSVFileWriterService:

    def get_fake_data(self, fields: List[Dict[str, Any]], row_nums: int) -> List:
        data_to_csv = FakeDataGeneratorService().generate_fake_data(fields=fields, row_nums=row_nums)
        return data_to_csv

    def create_csv_file_with_fake_data(self, row_nums: int, schema: Dict, file_name: str):
        column_separator = schema.column_separator
        string_character = schema.string_character
        data_to_csv = self.get_fake_data(fields=schema.fields, row_nums=row_nums)
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


class FakeDataGeneratorService:

    def __init__(self):
        self.faker = Faker()

    def generate_fake_data(self, fields: List[Dict[str, Any]], row_nums: int) -> List:
        generated_data = []
        for i in range(row_nums):
            column = {}
            for item in fields:
                name = item["name"]
                if item["type"] == "integer":
                    column[name] = random.randint(
                        int(item["value_from"]), int(item["value_to"])
                    )
                    continue
                column_type = getattr(self.faker, item["type"])
                column[name] = column_type()
            generated_data.append(column)
        return generated_data
