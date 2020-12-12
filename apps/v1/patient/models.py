from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.v1.common.models import BaseModel
from apps.v1.myauth.models import Account, UserManager
from apps.v1.health_institution.models import HealthInstitution

# Create your models here.
class Patient(BaseModel):
    id = None
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    nik = models.CharField(max_length=16, null = True)

    class PhysicalActivityType(models.IntegerChoices):
        LIGHT = 1, _('Light')
        MODERATE = 2, _('Moderate')
        HEAVY = 3, _('Heavy')
        VERY_HEAVY = 4, _('Very Heavy')
    physical_activity_type = models.IntegerField(
        choices = PhysicalActivityType.choices,
        default = PhysicalActivityType.LIGHT,
    )

    smoke_amount = models.PositiveIntegerField(default = 0)

    health_institution = models.ForeignKey(HealthInstitution, on_delete=models.CASCADE)
    is_male = models.BooleanField()
    height = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999),
        ],
        default = 0,
    )
    weight = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999),
        ],
        default = 0,
    )
    
@receiver(models.signals.pre_save, sender=Patient)
def set_role(sender, instance, *args, **kwargs):
    instance.account.role = Account.Role.PATIENT
    instance.account.save()
    return instance

@receiver(models.signals.post_delete, sender=Patient)
def remove_account(sender, instance, *args, **kwargs):
    if instance != None:
        instance.account.delete()

