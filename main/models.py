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

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    