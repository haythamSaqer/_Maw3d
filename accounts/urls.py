from django.urls import path, include
from .views import get

urlpatterns = [
    path('', get)
]
