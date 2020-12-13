from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.LungSoundClassificationViewSet, 'lung-sound-classifications')

urlpatterns = [
    # path('untaken/', views.untaken_classifications),
    path('', include(router.urls)),
]