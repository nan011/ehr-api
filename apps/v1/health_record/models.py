from django.db import models

from apps.v1.common.models import BaseModel
from apps.v1.myauth.models import User

# Create your models here.
class HealthRecord(BaseModel):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    do_activity = models.BooleanField()
    do_smoke = models.BooleanField()
    take_medicine = models.BooleanField()
    have_family_illness = models.BooleanField()

    sistole = models.FloatField()
    diastole = models.FloatField()

    blood_sugar_level = models.FloatField()

    height = models.FloatField()
    weight = models.FloatField()
    waist_size = models.FloatField()

    cholesterol_level = models.FloatField()
    blood_volume = models.FloatField()

    oxygen_saturation = models.FloatField()
    oxygen_volume = models.FloatField()
    lung_sounds = models.FileField()

    cardiovascular_risk = models.FloatField()
    diabetes_risk = models.FloatField()
