# from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Application, Contract

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

import json

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!! Надо добавить поле пользователь в модель Application!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_contract(request, id):
    contract = Contract.objects.filter(id=id)
    return JsonResponse({'document': [contract.name, contract.text]}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_contract(request):
    data = json.loads(request.body)
    user = request.user
    try:
        contract = Contract.objects.create(
            name=data["name"],
            text=data["text"]
        )
        return JsonResponse({'document': [contract.name, contract.text]}, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_contract(request, id):
    user = request.user.id
    payload = json.loads(request.body)
    try:
        contract_item = Contract.objects.filter(id=id)
        contract_item.update(**payload)
        contract = Contract.objects.get(id=id)
        return JsonResponse({'contract': [contract.name, contract.text]}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_contract(request, id):
    user = request.user.id
    try:
        contract = Contract.objects.get(id=id)
        contract.delete()
        return JsonResponse({'result': 'contract deleted'}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_application(request, id):
    application = Application.objects.filter(id=id)
    return JsonResponse({'Application': [application.number, application.date_of_contract]}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_application(request):
    data = json.loads(request.body)
    user = request.user
    try:
        contract = Contract.objects.get(id=data["contract"])
        application = Application.objects.create(
            number=data["number"],
            contract=contract,
            inn=data["inn"],
            test_object=data["test_object"],
            defined_characteristic=data["defined_characteristic"],
            amount=data["amount"],
            type_of_documentation=data["type_of_documentation"]
        )
        return JsonResponse({'Application': [application.number, application.date_of_contract]}, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_application(request, id):
    user = request.user.id
    payload = json.loads(request.body)
    try:
        application_item = Application.objects.filter(id=id)
        application_item.update(**payload)
        application = Application.objects.get(id=id)
        return JsonResponse({'Application': [application.number, application.date_of_contract]}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_application(request, id):
    user = request.user.id
    try:
        application = application.objects.get(id=id)
        application.delete()
        return JsonResponse({'result': 'application deleted'}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    