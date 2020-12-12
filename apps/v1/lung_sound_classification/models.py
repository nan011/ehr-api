import random

from django.db import models, utils
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from apps.v1.common.models import BaseModel

# Create your models here.
class LungSoundClassification(BaseModel):
    reserved_id = models.PositiveIntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(9999),
        ],
        unique=True,
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
def generate_reserved_id(sender, instance, *args, **kwargs):
    if instance._state.adding:
        while True:
            try:
                instance.reserved_id = random.randint(0, 9999)
                instance.full_clean()
            except ValidationError as e:
                if e.error_dict['reserved_id'] is None:
                    break
            else:
                break