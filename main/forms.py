from django.forms import ModelForm

from .models import Application, Contract


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields=['name', 'text']

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['number', 'contract', 'date_of_contract', 'inn', 'test_object', 'defined_characteristic', 'amount', 'type_of_documentation']
