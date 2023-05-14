from django.db import models
# import datetime

class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)
    date_of_contract = models.DateField()
    inn = models.CharField(max_length=30)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    test_object = models.CharField(max_length=20)
    defined_characteristic = models.CharField(max_length=100)
    amount = models.IntegerField()
    type_of_documentation = models.CharField(max_length=20)

# Create your models here.

class Contract(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=500)

def create_application():
    Application.objects.create()

def read_application(number):
    return Application.objects.get(number=number)

def update_application(number, number_new, contract, d_od_c, inn, cust, t_o, def_ch, amount, type_of_documentation):
    app = Application.objects.get(number=number)
    app.number = number_new
    app.contract = contract
    app.date_of_contract = d_od_c
    app.inn = inn
    app.customer = cust
    app.test_object = t_o
    app.defined_characteristic = def_ch
    app.amount = amount
    app.type_of_documentation = type_of_documentation
    app.save()

def delete_application(number):
    Application.objects.get(number=number).delete()

def create_contract():
    Contract.objects.create()

def read_contract(name):
    return Contract.objects.get(name=name)

def update_contract(name, name_new, text):
    con = Contract.objects.get(name=name)
    con.name = name_new
    con.text = text

def delete_contract(name):
    Contract.objects.get(name=name).delete()