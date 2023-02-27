import uuid

from faker import Faker
from typing import Any, Dict, List
from faker.generator import random

fake = Faker()


def generate_fake_data(data: List[Dict[str, Any]], row_nums: str) -> List:
    generated_data = []
    for i in range(int(row_nums)):
        column = {}
        for item in data:
            name = item["name"]
            if item["type"] == "integer":
                column[name] = random.randint(
                    int(item["value_from"]), int(item["value_to"])
                )
            if item["type"] != "integer":
                column_type = getattr(fake, item["type"])
                column[name] = column_type()
        generated_data.append(column)
    return generated_data


def generate_cache_task_key():
    return str(uuid.uuid1())
