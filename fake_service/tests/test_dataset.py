import uuid

from rest_framework.test import APITestCase
from rest_framework import status
from schema.models import Schema, Dataset
from django.contrib.auth.models import User
from django.test.utils import override_settings


class DatasetCreateTestCase(APITestCase):

    def setUp(self):
        self.schema_name = str(uuid.uuid1())
        self.columns_data = [
            {"name": "column_1", "type": "job"},
            {"name": "column_2", "type": "phone_number"},
            {"name": "column_3", "type": "integer", "value_from": 1, "value_to": 50},
        ]
        self.user = User.objects.create_user(
            username="user", password="qwerty"
        )
        self.schema = Schema.objects.create(
            user=self.user,
            name=self.schema_name,
            column_separator=".",
            string_character='"',
            fields=self.columns_data,
        )
        self.client.force_authenticate(user=self.user)

    @override_settings(
        CELERY_TASK_EAGER_PROPAGATES=True,
        CELERY_TASK_ALWAYS_EAGER=True,
        BROKER_BACKEND="memory",
    )
    def test_create_dataset(self):

        url = f"http://127.0.0.1:8000/api/schema/{self.schema.pk}/generate_data/?count=50"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dataset.objects.all().count(), 1)
        last_dataset = Dataset.objects.last()
        self.assertEqual(last_dataset.file.name, f"datasets/{self.schema_name}.csv")
