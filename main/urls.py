from django.urls import path

from .views import (ContractDetailView, ContractListView, CreateContractView,
                    SignUp, about, contract, home, index)

urlpatterns = [
    path('', index),
    path('about/', about),
    path('signup/', SignUp.as_view()),
    path('home/', home),
    path('contract', contract, name='contract'),
    path('contract/create', CreateContractView.as_view(), name='contract_create'),
    path('contract/list', ContractListView.as_view(), name='contract_list'),
    path('contract/list/<int:pk>', ContractDetailView.as_view(), name='contract_detail'),
]
