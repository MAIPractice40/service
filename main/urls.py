from django.urls import path

from .views import (
    SignUp, about, home, index, 
    get_contract, add_contract, update_contract, delete_contract,
    get_application, add_application, update_application, delete_application
)
    

urlpatterns = [
    path('', index),
    path('about/', about),
    path('signup/', SignUp.as_view()),
    path('home/', home),
    path('crud/get-contract/<int:id>/', get_contract),
    path('crud/add-contract/', add_contract),
    path('crud/update-contract/<int:id>', update_contract),
    path('crud/delete-contract/<int:id>', delete_contract),
    path('crud/get-application/<int:id>/', get_application),
    path('crud/add-application/', add_application),
    path('crud/update-application/<int:id>', update_application),
    path('crud/delete-application/<int:id>', delete_application),
]
