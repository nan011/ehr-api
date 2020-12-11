import uuid

from django.forms.models import model_to_dict
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

class BaseManager(models.Manager):
    def create_raw(self, *args, **kwargs):
        return self.model(*args, **kwargs)

class BaseModel(models.Model):
    objects = BaseManager()

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

    def values(self):
        return model_to_dict(self)

    class Meta:
        abstract = True