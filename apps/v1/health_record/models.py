from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from apps.v1.common.models import BaseModel
from apps.v1.patient.models import Patient

RANGE_0_100 = [
    MinValueValidator(0),
    MaxValueValidator(100),
]

RANGE_0_999 = [
    MinValueValidator(0),
    MaxValueValidator(999),
]

# Create your models here.
class HealthRecord(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    do_activity = models.BooleanField(default=False)
    do_smoke = models.BooleanField(default=False)
    take_medicine = models.BooleanField(default=False)
    have_medical_history = models.BooleanField(default=False)

    sistole = models.FloatField(validators=RANGE_0_999, default=0)
    diastole = models.FloatField(validators=RANGE_0_999, default=0)
    blood_sugar_level = models.FloatField(validators=RANGE_0_999, default=0)
    height = models.FloatField(validators=RANGE_0_999, default=0)
    weight = models.FloatField(validators=RANGE_0_999, default=0)
    waist_size = models.FloatField(validators=RANGE_0_999, default=0)
    cholesterol_total = models.FloatField(validators=RANGE_0_999, default=0)
    oxygen_saturation = models.FloatField(validators=RANGE_0_100, default=0)
    cardiovascular_risk = models.FloatField(validators=RANGE_0_100, default=0)
    diabetes_risk = models.FloatField(validators=RANGE_0_100, default=0)
