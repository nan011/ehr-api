from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.OperatorViewSet, 'operators')

urlpatterns = [
    path('', include(router.urls))
]