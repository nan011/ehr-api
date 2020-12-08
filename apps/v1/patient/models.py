from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.v1.myauth.models import User, UserManager
from apps.v1.health_institution.models import HealthInstitution

# Create your models here.
class UserManager(UserManager):
    def create_user(self, **kwargs):
        user = super().create_user(
            kwargs.pop('email'),
            kwargs.pop('password'),
            **kwargs,
        )
        user.role = User.Role.PATIENT
        user.save()
        return user

class Patient(User):
    objects = UserManager()
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


