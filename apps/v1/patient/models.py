from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from apps.v1.common.models import BaseModel
from apps.v1.myauth.models import Account, UserManager
from apps.v1.health_institution.models import HealthInstitution

# Create your models here.
class Patient(BaseModel):
    id = None
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    nik = models.CharField(max_length=16)

    class PhysicalActivityType(models.IntegerChoices):
        UNKNOWN = 0, _('Unknown')
        EXTREMELY_INACTIVE = 1, _('Extremely Inactive')
        SEDENTARY = 2, _('Sedentary')
        MODERATELY_ACTIVE = 3, _('Moderately Active')
        VIGOROUSLY_ACTIVE = 4, _('Vigorously Active')
        EXTREMELY_ACTIVE = 5, _('Extremely Active')
    physical_activity_type = models.IntegerField(
        choices = PhysicalActivityType.choices,
        default = PhysicalActivityType.UNKNOWN,
    )

    smoke_amount = models.PositiveIntegerField()
    
    # class FamilyPosition(models.IntegerChoices):
    #     FATHER = 1, _('Father')
    #     MOTHER = 2, _('Mother')
    #     GRANDFATHER = 3, _('Grandfather')
    #     GRANDMOTHER = 4, _('Grandmother')
    # family_position = models.IntegerField(
    #     choices = FamilyPosition.choices
    #     default = FamilyPosition.FATHER
    # )
    # medical_history = models.TextField(max_length = 2000)

    health_institution = models.ForeignKey(HealthInstitution, on_delete=models.CASCADE)
    is_male = models.BooleanField()
    height = models.FloatField()
    weight = models.FloatField()
    
@receiver(models.signals.pre_save, sender=Patient)
def set_role(sender, instance, *args, **kwargs):
    instance.account.role = Account.Role.PATIENT
    instance.account.save()
    return instance

@receiver(models.signals.pre_delete, sender=Patient)
def remove_role(sender, instance, *args, **kwargs):
    instance.account.role = Account.Role.UNKNOWN
    instance.account.save()
    return instance

