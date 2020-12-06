import uuid

from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
    )

    created_at = models.DateTimeField(
        verbose_name = "Created at",
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = "Updated at",
        auto_now = True,
    )