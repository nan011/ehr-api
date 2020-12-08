from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

medicine_router = DefaultRouter()
medicine_router.register('', views.MedicineViewSet, 'medicines')

medicine_type_router = DefaultRouter()
medicine_type_router.register('', views.MedicineTypeViewSet, 'types')

urlpatterns = [
    path('types/', include(medicine_type_router.urls)),
    path('', include(medicine_router.urls)),
]