from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.HealthRecordViewSet, 'health-records')

urlpatterns = [
    path('untaken/', views.untaken_records),
    path('<slug:pk>/redeem/', views.redeem),
    path('', include(router.urls)),
]