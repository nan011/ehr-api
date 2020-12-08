from django.db import models

from apps.v1.common.models import BaseModel
from apps.v1.patient.models import Patient 

# Create your models here.
class MedicineType(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Medicine(BaseModel):
    patient = models.ForeignKey(Patient, related_name = 'medicines', on_delete=models.CASCADE)
    type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    frequency = models.PositiveIntegerField(default = 0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
