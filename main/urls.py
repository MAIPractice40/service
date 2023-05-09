from django.urls import path

from .views import SignUp, about, home, index

urlpatterns = [
    path('', index),
    path('about/', about),
    path('signup/', SignUp.as_view()),
    path('home/', home)
]
