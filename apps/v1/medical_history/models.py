from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.v1.common.models import BaseModel
from apps.v1.patient.models import Patient

# Create your models here.
class MedicalHistory(BaseModel):
    patient = models.ForeignKey(Patient, related_name='medical_histories', on_delete=models.CASCADE)

    class RelationshipType(models.IntegerChoices):
        FATHER = 1, _("Father")
        MOTHER = 2, _("Mother")
    relationship = models.PositiveSmallIntegerField(
        choices = RelationshipType.choices,
    )

    description = models.TextField(max_length = 2000)

    class Meta:
        unique_together = (('patient', 'relationship'),)
        verbose_name_plural = 'medical histories'