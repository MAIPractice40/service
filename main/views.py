from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import ApplicationForm, ContractForm
from .models import Contract

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!! Надо добавить поле пользователь в модель Application!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def index(request):
    return HttpResponse('This is index page')

def about(request):
    return HttpResponse('This is about page')

def home(request):
    return render(request,"main/home.html")

def contract(request):
    return render(request,"main/crud/contracts.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CreateContractView(LoginRequiredMixin,CreateView):
    login_url ="/accounts/login/"
    success_url = reverse_lazy("contract_create")
    form_class = ContractForm
    template_name = "main/crud/create_contract.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateContractView, self).form_valid(form)

class ContractListView(LoginRequiredMixin,ListView):
    login_url ="/accounts/login/"
    model= Contract
    template_name = "main/crud/contract_list.html"

    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)

class ContractDetailView(LoginRequiredMixin, DetailView):
    login_url ="/accounts/login/"
    model= Contract
    template_name = "main/crud/contract_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object'].user.id != self.request.user.id:
            raise PermissionDenied
        return context
