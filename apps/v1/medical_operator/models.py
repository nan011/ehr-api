from django.db import models
from apps.v1.health_institution.models import HealthInstitution
from django.core.validators import RegexValidator
from django.dispatch import receiver

from apps.v1.common.models import BaseModel
from apps.v1.myauth.models import Account, UserManager

# Create your models here.
class Operator(BaseModel):
    id = None
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

    birthday = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex = '^([1-9]|0[1-9]|[12]\d|3[0-1])\/([1-9]|0[1-9]|1[012])\/[1-9]\d+$',
                message = 'The format should be dd/mm/yyyy',
            ),
        ],
    )
    health_institution = models.ForeignKey(HealthInstitution, on_delete = models.CASCADE)
    phone_number = models.CharField(
        max_length = 15,
        validators = [
            RegexValidator(
                regex = '^\+[1-9]\d{1,2}\d{11,12}$',
                message = 'Invalid phone number',
            ),
        ],
    )
    
    
@receiver(models.signals.pre_save, sender=Operator)
def set_role(sender, instance, *args, **kwargs):
    instance.account.role = Account.Role.OPERATOR
    instance.account.save()
    return instance


@receiver(models.signals.post_delete, sender=Operator)
def remove_account(sender, instance, *args, **kwargs):
    if instance != None:
        instance.account.delete()