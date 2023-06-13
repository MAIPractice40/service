from django.urls import path

from .dash_apps import app1
from .views import (ApplicationDetailView, ApplicationListView,
                    ContractDetailView, ContractListView,
                    CreateApplicationView, CreateContractView, SignUp, about,
                    dash_demo, home, index)

urlpatterns = [
    path('', index),
    path('about/', about),
    path('signup/', SignUp.as_view()),
    path('home/', home),
    path('contract/create', CreateContractView.as_view(), name='contract_create'),
    path('contract/list', ContractListView.as_view(), name='contract_list'),
    path('contract/list/<int:pk>', ContractDetailView.as_view(), name='contract_detail'),
    # path('application/create', CreateApplicationView.as_view(), name='application_create'),
    # path('application/list', ApplicationListView.as_view(), name='application_list'),
    # path('application/list/<int:pk>', ApplicationDetailView.as_view(), name='application_detail'),
    path('app1/', dash_demo)
]
