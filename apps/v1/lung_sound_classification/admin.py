from django.contrib import admin

from .models import LungSoundClassification

# Register your models here.
class LungSoundClassificationAdmin(admin.ModelAdmin):
    list_display = ('reserved_id', 'likelihood_percentage', 'result')
    exclude = ('reserved_id',)

admin.site.register(LungSoundClassification, LungSoundClassificationAdmin)