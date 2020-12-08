from django.contrib import admin

from .models import MedicineType, Medicine

# # Register your models here.
admin.site.register(MedicineType)
admin.site.register(Medicine)