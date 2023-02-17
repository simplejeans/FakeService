from django.contrib.auth import get_user_model
from django.db import models
from .choices import SCHEMA_COLUMN_SEPARATOR, SCHEMA_STRING_CHARACTER

User = get_user_model()


class Schema(models.Model):
    user = models.ForeignKey(
        User, related_name="data_schemas", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    column_separator = models.CharField(max_length=255, choices=SCHEMA_COLUMN_SEPARATOR)
    string_character = models.CharField(max_length=255, choices=SCHEMA_STRING_CHARACTER)
    updated_at = models.DateTimeField(auto_now=True)
    fields = models.JSONField(blank=False, null=False)

    def __str__(self):
        return self.name