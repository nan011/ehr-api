from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.v1.myauth.urls')),
    path('area/', include('apps.v1.area.urls')),
]