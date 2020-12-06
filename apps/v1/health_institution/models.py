from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from apps.v1.common.models import BaseModel
from apps.v1.area.models import Province, City

# Create your models here.
class HealthInstitution(BaseModel):
    basemodel_ptr = models.OneToOneField(
        to = BaseModel,
        parent_link = True,
        related_name = "+",
        on_delete = models.CASCADE
    )

    name = models.CharField(max_length = 255)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField(max_length = 255)
    email = models.EmailField()
    website = models.URLField()

    def __str__(self):
        return self.name

@receiver(pre_save, sender=HealthInstitution)
def check_province_and_city_consistency(sender, instance, *args, **kwargs):
    if instance.city.province.id != instance.province.id:
        raise ValidationError("{} doesn't belong to {}".format(instance.city.name, instance.province.name))