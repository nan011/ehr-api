from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:pk>/activate/', views.activate),
    path('users/<str:pk>/deactivate/', views.deactivate),
    path('token/', views.AuthToken.as_view()),
]