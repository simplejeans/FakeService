from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from schema.models import User, Schema


class SchemaApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="alabama", password="password")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.post = Schema.objects.create(
            user=self.user,
            name="qwerty228",
            column_separator=".",
            string_character="'",
            fields=[
                {
                    "name": "qwertty228",
                    "type": "integer",
                    "value_from": "20",
                    "value_to": "34",
                }
            ],
        )

    def test_post(self):
        sample_post = {
            "name": "Schema_2",
            "column_separator": ",",
            "string_character": "'",
            "fields": [
                {
                    "name": "Column_1",
                    "type": "integer",
                    "value_from": "1",
                    "value_to": "20",
                }
            ],
        }

        response = self.client.post(reverse("schema-list"), sample_post, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        updating_post = {
            "id": 1,
            "name": "qwerty2228",
            "column_separator": ".",
            "string_character": "'",
            "fields": [
                {
                    "name": "qwertty228",
                    "type": "integer",
                    "value_from": 20,
                    "value_to": 34,
                }
            ],
        }
        url = "http://127.0.0.1:8000/api/schema/1/"
        response = self.client.patch(url, data={"name": "qwerty2228"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), updating_post)
