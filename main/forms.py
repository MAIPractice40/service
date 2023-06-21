from django.forms import ModelForm
from django import forms

from .models import Application, Contract


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['title', 'text', 'date_of_contract', 'data_file']
        widgets = {
            'date_of_contract': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['number', 'contract', 'date_of_contract', 'inn', 'test_object', 'defined_characteristic', 'amount',
                  'type_of_documentation']
