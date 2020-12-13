import random

from django.db import models, utils
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from apps.v1.common.models import BaseModel
from apps.v1.health_record.models import HealthRecord
from .constants import RESERVED_IDS


# Create your models here.
class ReservedID(models.Model):
    id = models.PositiveSmallIntegerField(
        validators = [
            MinValueValidator(RESERVED_IDS[0]),
            MaxValueValidator(RESERVED_IDS[-1]),
        ],
        primary_key = True,
    )

class LungSoundClassification(BaseModel):
    reserved_id = models.OneToOneField(
        ReservedID,
        related_name = "lung_sound_classification",
        on_delete=models.SET_NULL,
        null = True,
    )
    health_record = models.OneToOneField(
        HealthRecord,
        related_name = "lung_sound_classification",
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
    )

    class ResultType(models.IntegerChoices):
        UNCLASSIFIED = 99, _('Unclassified')
        CRACKLES = 1, _('Crackles')
        WHEEZING = 2, _('Wheezing')

    likelihood_percentage = models.FloatField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    result = models.PositiveSmallIntegerField(choices=ResultType.choices)

@receiver(models.signals.pre_save, sender=LungSoundClassification)
def book_reserved_id(sender, instance, *args, **kwargs):
    if instance._state.adding:
        instance.reserved_id = ReservedID.objects.filter(lung_sound_classification = None)[0]

@receiver(models.signals.pre_save, sender=LungSoundClassification)
def unbook_reserved_id(sender, instance, *args, **kwargs):
    if instance.health_record is not None:
        instance.reserved_id = None

    