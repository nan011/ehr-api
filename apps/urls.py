from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.v1.urls')),
]