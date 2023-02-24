import uuid

from faker import Faker
from typing import Any, Dict, List
from faker.generator import random

fake = Faker()


def make_generetions(data: List, count: str) -> List:
    list2 = []
    for i in range(int(count)):
        dict1 = {}
        for item in data:
            name = item["name"]
            if item["type"] == "integer":
                dict1[name] = random.randint(
                    int(item["value_from"]), int(item["value_to"])
                )
            if item["type"] != "integer":
                column_type = getattr(fake, item["type"])
                dict1[name] = column_type()
        list2.append(dict1)
    return list2


def generate_cache_task_key():
    return str(uuid.uuid1())
