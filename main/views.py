# from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.

def index(request):
    return HttpResponse('This is index page')

def about(request):
    return HttpResponse('This is about page')

def home(request):
    return render(request,"main/home.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
