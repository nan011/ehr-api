from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

# Create your models here.
class BaseQuerySet(QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()

    def hard_delete(self):
        for obj in self:
            obj.hard_delete()

class BaseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BaseQuerySet(
            model = self.model,
            using = self._db,
            hints = self._hints,
        ).filter(deleted_at=None)

    def get(self, *args, **kwargs):
        return self.get_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name = "Created at",
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = "Updated at",
        auto_now = True,
    )

    deleted_at = models.DateTimeField(
        blank = True,
        null = True,
        verbose_name = "Deleted at",
    )

    objects = BaseManager()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(Base, self).delete()