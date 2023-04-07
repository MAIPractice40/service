from .views import index, about
from django.urls import path

urlpatterns = [
    path('', index),
    path('about/', about)
]