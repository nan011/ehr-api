from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.v1.myauth.urls')),
    path('area/', include('apps.v1.area.urls')),
    path('health-institutions/', include('apps.v1.health_institution.urls')),
    path('operators/', include('apps.v1.medical_operator.urls')),
]