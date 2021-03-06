from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.v1.myauth.urls')),
    path('area/', include('apps.v1.area.urls')),
    path('health-institutions/', include('apps.v1.health_institution.urls')),
    path('operators/', include('apps.v1.medical_operator.urls')),
    path('patients/', include('apps.v1.patient.urls')),
    path('medicines/', include('apps.v1.medicine.urls')),
    path('health-records/', include('apps.v1.health_record.urls')),
    path('medical-histories/', include('apps.v1.medical_history.urls')),
    path('lung-sound-classifications/', include('apps.v1.lung_sound_classification.urls')),
]