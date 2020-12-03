from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.AuthToken.as_view()),
]