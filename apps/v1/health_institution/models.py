from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from apps.v1.common.models import BaseModel
from apps.v1.area.models import Province, City

# Create your models here.
class HealthInstitution(BaseModel):
    name = models.CharField(max_length = 255, unique=True)
    address = models.TextField(max_length = 255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null = True)
    email = models.EmailField(null = True)
    website = models.URLField(null = True)

    def __str__(self):
        return self.name