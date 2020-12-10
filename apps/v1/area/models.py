from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.v1.common.models import BaseModel
from apps.v1.common.tools import capitalize

# Create your models here.
class Province(BaseModel):
    name = models.CharField(_("name"), max_length = 255)

    def __str__(self):
        return self.name

class City(BaseModel):
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length = 255)
    
    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Province)
@receiver(pre_save, sender=City)
def fix_name(sender, instance, *args, **kwargs):
    instance.name = capitalize(instance.name)