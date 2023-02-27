from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from schema.models import User, Schema


class SchemaApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="alabama", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Schema.objects.create(
            user=self.user,
            name="qwerty228",
            column_separator=".",
            string_character="'",
            fields=[
                {
                    "name": "qwertty228",
                    "type": "integer",
                    "value_from": 20,
                    "value_to": 34,
                }
            ],
        )

    def test_create_schema(self):
        sample_schema = {
            "name": "Schema_2",
            "column_separator": ",",
            "string_character": "'",
            "fields": [{"name": "Column_1",
                        "type": "integer",
                        "value_from": 1,
                        "value_to": 20}]}

        url = "http://127.0.0.1:8000/api/schema/"
        response = self.client.post(url, sample_schema, format="json")
        created_schema = Schema.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_schema.name, sample_schema["name"])

    def test_update(self):
        updating_schema = {
            "id": 1,
            "name": "qwerqwerqetrewrt",
            "column_separator": ".",
            "string_character": "'",
            "fields": [
                {
                    "name": "qwertyqwertyqetr",
                    "type": "job",
                }
            ],
        }
        url = "http://127.0.0.1:8000/api/schema/1/"
        response = self.client.patch(url, updating_schema, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), updating_schema)
