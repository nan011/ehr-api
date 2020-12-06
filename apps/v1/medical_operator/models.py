from django.db import models
from apps.v1.health_institution.models import HealthInstitution
from django.core.validators import RegexValidator

from apps.v1.myauth.models import User, UserManager

# Create your models here.
class OperatorManager(UserManager):
    def create_user(self, **kwargs):
        user = super().create_user(
            kwargs.pop('email'),
            kwargs.pop('password'),
            **kwargs,
        )
        user.role = User.Role.OPERATOR
        user.save()
        return user

class Operator(User):
    objects = OperatorManager()

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
    